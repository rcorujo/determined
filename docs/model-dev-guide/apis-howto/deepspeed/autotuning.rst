.. _deepspeed-autotuning:

################################
 DeepSpeed Autotune: User Guide
################################

.. meta::
   :description: This user guide demonstrates how to optimize DeepSpeed parameters in order to take full advantage of the user's hardware and model.

Getting the most out of DeepSpeed (DS) requires aligning the many DS parameters with the specific
properties of your hardware and model. Determined AI's DeepSpeed Autotune (``dsat``) helps to
optimize these settings through an easy-to-use API with very few changes required in user-code, as
we describe in the remainder of this user guide. ``dsat`` can be used with
:class:`~determined.pytorch.deepspeed.DeepSpeedTrial`, :ref:`Core API <core-getting-started>`, and
`HuggingFace Trainer <https://huggingface.co/docs/transformers/main_classes/trainer>`__.

**************
 How it Works
**************

You do not need to create a special configuration file to use ``dsat``. Assuming you have DeepSpeed
code which already functions, autotuning is as easy as inserting one or two helper functions into
your code and modifying the launch command.

For instance, let's say your directory contains DeepSpeed code and a corresponding ``single`` trial
experiment configuration file ``deepspeed.yaml``. Then, after inserting a line or two of
``dsat``-specific code per the instructions in the following sections, launching the ``dsat``
experiments is as easy as replacing the usual experiment-launching command:

.. code::

   det experiment create deepspeed.yaml .

with:

.. code::

   python3 -m determined.pytorch.dsat asha deepspeed.yaml .

The above uses Determined AI's DeepSpeed Autotune with the ``asha`` algorithm, one of three
available search methods:

-  ``asha``: Adaptively searches over randomly selected DeepSpeed configurations, allocating more
   compute resources to well-performing configurations. See :ref:`this introduction to ASHA
   <topic-guides_hp-tuning-det_adaptive-asha>` for more details.

-  ``binary``: Performs a simple binary search over the batch size for randomly-generated DS
   configurations.

-  ``random``: Conducts a search over random DeepSpeed configurations with an aggressive
   early-stopping criteria based on domain-knowledge of DeepSpeed and the search history.

DeepSpeed Autotune is built on top of Custom Searcher (see :ref:`topic-guides_hp-tuning-det_custom`)
which starts up two separate experiments:

-  ``single`` Search Runner Experiment: This experiment coordinates and schedules the trials that
   run the model code.
-  ``custom`` Experiment: This experiment contains the trials referenced above whose results are
   reported back to the search runner.

Initially, a profiling trial is created to gather information regarding the model and computational
resources. The search runner experiment takes this initial profiling information and creates a
series of trials to search for the DS settings which optimize ``FLOPS_per_gpu``, ``throughput``
(samples/second), or latency timing information. The results of all such trials can be viewed in the
``custom`` experiment above. The search is informed both by the initial profiling trial and the
results of each subsequent trial, all of whose results are fed back to the search runner.

.. warning::

   Determined's DeepSpeed Autotune is not compatible with pipeline or model parallelism. The
   to-be-trained model must be a ``DeepSpeedEngine`` instance (not a ``PipelineEngine`` instance).

*******************
 User Code Changes
*******************

To use ``dsat`` with :class:`~determined.pytorch.deepspeed.DeepSpeedTrial`, Core API, and
HuggingFace Trainer, specific changes must be made to your user code. In the following sections, we
will describe specific use cases and the changes needed for each.

.. _using_deepspeed_trial:

DeepSpeedTrial
==============

To use Determined's DeepSpeed Autotune with ``DeepSpeedTrial``, you must meet the following
requirements.

First, it is assumed that a base DeepSpeed configuration exists in a file (written following the
`DeepSpeed documentation here <https://www.deepspeed.ai/docs/config-json/>`_). We then require that
your Determined ``yaml`` configuration points to the location of that file through a
``deepspeed_config`` key in its ``hyperparameters`` section. For example, if your default DeepSpeed
configuration is stored in ``ds_config.json`` at the top-level of your model directory, your
``hyperparameters`` section should include:

.. code:: yaml

   hyperparameters:
     deepspeed_config: ds_config.json

Second, your ``DeepSpeedTrial`` code must use our
:func:`~determined.pytorch.dsat.get_ds_config_from_hparams` helper function to get the DeepSpeed
configuration dictionary which is generated by DeepSpeed Autotune for each trial. These dictionaries
are generated by overwriting certain fields in the base DeepSpeed configuration referenced in the
step above. The returned dictionary can then be passed to ``deepspeed.initialize`` as usual:

.. code:: python

   from determined.pytorch.deepspeed import DeepSpeedTrial, DeepSpeedTrialContext
   from determined.pytorch import dsat


   class MyDeepSpeedTrial(DeepSpeedTrial):
     def __init__(self, context: DeepSpeedTrialContext) -> None:
         self.hparams = self.context.get_hparams()
         config = dsat.get_ds_config_from_hparams(self.hparams)
         model = ...
         model_parameters= ...

         model_engine, optimizer, train_loader, lr_scheduler = deepspeed.initialize(
             model=model, model_parameters=model_parameters, config=config
         )

Using Determined's DeepSpeed Autotune with a :class:`~determined.pytorch.deepspeed.DeepSpeedTrial`
instance requires no further changes to your code.

For a complete example of how to use DeepSpeed Autotune with ``DeepSpeedTrial``, visit the
`Determined GitHub Repo
<https://github.com/determined-ai/determined/tree/master/examples/deepspeed_autotune/torchvision/deepspeed_trial>`__
and navigate to ``examples/deepspeed_autotune/torchvision/deepspeed_trial`` .

.. note::

   To find out more about ``DeepSpeedTrial``, visit :ref:`deepspeed-api`.

Core API
========

When using DeepSpeed Autotune with a Core API experiment, there is one additional change to be made
following the steps in the :ref:`using_deepspeed_trial` section above.

The ``forward``, ``backward``, and ``step`` methods of the ``DeepSpeedEngine`` class need to be
wrapped in the :func:`~determined.pytorch.dsat.dsat_reporting_context` context manager. This
addition ensures that the autotuning metrics from each trial are captured and reported back to the
Determined master.

Here is an example sketch of ``dsat`` code with Core API:

.. code:: python

   for op in core_context.searcher.operations():
      for (inputs, labels) in trainloader:
          with dsat.dsat_reporting_context(core_context, op): # <-- The new code
              outputs = model_engine(inputs)
              loss = criterion(outputs, labels)
              model_engine.backward(loss)
              model_engine.step()

In this code snippet, ``core_context`` is the :class:`~determined.core.Context` instance which was
initialized with :func:`determined.core.init`. The context manager requires access to both
``core_context`` and the current :class:`~determined.core.SearcherOperation` instance (``op``) to
appropriately report results. Outside of a ``dsat`` context, ``dsat_reporting_context`` is a no-op,
so there is no need to remove the context manager after the ``dsat`` trials have completed.

For a complete example of how to use DeepSpeed Autotune with Core API, visit the `Determined GitHub
Repo
<https://github.com/determined-ai/determined/tree/master/examples/deepspeed_autotune/torchvision/core_api>`__
and navigate to ``examples/deepspeed_autotune/torchvision/core_api`` .

HuggingFace Trainer
===================

You can also use Determined's DeepSpeed Autotune with the HuggingFace (HF) Trainer and Determined's
:class:`~determined.transformers.DetCallback` callback object to optimize your DeepSpeed parameters.

Similar to the previous case (Core API), you need to add a ``deepspeed_config`` field to the
``hyperparameters`` section of your experiment configuration file, specifying the relative path to
the DS ``json`` config file.

Reporting results back to the Determined master requires both the ``dsat.dsat_reporting_context``
context manager and ``DetCallback``.

Furthermore, since ``dsat`` performs a search over different batch sizes and HuggingFace expects
parameters to be specified as command-line arguments, an additional helper function,
:func:`~determined.pytorch.dsat.get_hf_args_with_overwrites`, is needed to create consistent
HuggingFace arguments.

Here is an example code snippet from a HuggingFace Trainer script that contains key pieces of
relevant code:

.. code:: python

   from determined.transformers import DetCallback
   from determined.pytorch import dsat
   from transformers import HfArgumentParser,Trainer, TrainingArguments,

   hparams = self.context.get_hparams()
   parser = HfArgumentParser(TrainingArguments)
   args = sys.argv[1:]
   args = dsat.get_hf_args_with_overwrites(args, hparams)
   training_args = parser.parse_args_into_dataclasses(args, look_for_args_file=False)

   det_callback = DetCallback(core_context, ...)
   trainer = Trainer(args=training_args, ...)
   with dsat.dsat_reporting_context(core_context, op=det_callback.current_op):
       train_result = trainer.train(resume_from_checkpoint=checkpoint)

.. important::

   -  The ``dsat_reporting_context`` context manager shares the same initial
      :class:`~determined.core.SearcherOperation` as the ``DetCallback`` instance through its
      ``op=det_callback.current_op`` argument.

   -  The entire ``train`` method of the HuggingFace trainer is wrapped in the
      ``dsat_reporting_context`` context manager.

To find examples that use DeepSpeed Autotune with HuggingFace Trainer, visit the `Determined GitHub
Repo <https://github.com/determined-ai/determined/tree/master/examples/hf_trainer_api>`__ and
navigate to ``examples/hf_trainer_api``.

******************
 Advanced Options
******************

The command-line entrypoint to ``dsat`` has various available options, some of them
search-algorithm-specific. All available options for any given search method can be found through
the command:

.. code::

   python3 -m determined.pytorch.dsat asha --help

and similar for the ``binary`` and ``random`` search methods.

Flags that are particularly important are detailed below.

General Options
===============

The following options are available for every search method.

-  ``--max-trials``: The maximum number of trials to run. Default: ``64``.

-  ``--max-concurrent-trials``: The maximum number of trials that can run concurrently. Default:
   ``16``.

-  ``--max-slots``: The maximum number of slots that can be used concurrently. Defaults to ``None``,
   i.e., there is no limit by default.

-  ``--metric``: The metric to be optimized. Defaults to ``FLOPS-per-gpu``. Other available options
   are ``throughput``, ``forward``, ``backward``, and ``latency``.

-  ``--run-full-experiment``: If specified, after the ``dsat`` experiment has completed, a
   ``single`` experiment will be launched using the specifications in the ``deepspeed.yaml``
   overwritten with the best-found DS configuration parameters.

-  ``--zero-stages``: This flag allows the user to limit the search to a subset of the stages by
   providing a space-separated list, as in ``--zero-stages 2 3``. Default: ``1 2 3``.

.. _asha-options:

``asha`` Options
================

The ``asha`` search algorithm randomly generates various DeepSpeed configurations and attempts to
tune the batch size for each configuration through a binary search. ``asha`` adaptively allocates
resources to explore each configuration (providing more resources to promising lineages) where the
resource is the number of steps taken in each binary search (i.e., the number of trials).

``asha`` can be configured with the following flags:

-  ``--max-rungs``: The maximum total number of rungs to use in the ASHA algorithm. Larger values
   allow for longer binary searches. Default: ``5``.

-  ``--min-binary-search-trials``: The minimum number of trials to use for each binary search. The
   ``r`` parameter in `the ASHA paper <https://arxiv.org/abs/1810.05934>`_. Default: ``3``.

-  ``--divisor``: Factor controlling the increased computational allotment across rungs, and the
   decrease in their population size. The ``eta`` parameter in `the ASHA paper
   <https://arxiv.org/abs/1810.05934>`_. Default: ``2``.

-  ``--search_range_factor``: The inclusive, initial ``hi`` bound on the binary search is set by an
   approximate computation (the ``lo`` bound is always initialized to ``1``). This parameter adjusts
   the ``hi`` bound by a factor of ``search_range_factor``. Default: ``1.0``.

``binary`` Options
==================

The ``binary`` search algorithm performs a straightforward search over the batch size for a
collection of randomly-drawn DS configurations. A single option is available for this search:
``--search_range_factor``, which plays precisely the same role as in the :ref:`asha-options` section
above.

``random`` Options
==================

The ``random`` search algorithm performs a search over randomly drawn DS configurations and uses a
semi-random search over the batch size.

``random`` can be configured with the following flags:

-  ``--trials_per_random_config``: The maximum batch size configuration which will tested for a
   given DS configuration. Default: ``5``.

-  ``--early-stopping``: If provided, the experiment will terminate if a new best-configuration has
   not been found in the last ``early-stopping`` trials. Default: ``None``, corresponding to no such
   early stopping.
