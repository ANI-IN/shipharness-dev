# Automated Unit Test Improvement using Large Language Models at Meta

Reading time: about 5 minutes.
Source: Alshahwan et al. (Meta), "Automated Unit Test Improvement using Large Language Models at Meta", FSE '24, 2024-02-14, <https://arxiv.org/abs/2402.09171> ([evidence](../../docs/evidence/s4.md#src-testgen-llm)).

> **Terms on this page**
>
> - **Test filters**: Five checks a test from the test phase must pass to be kept.
> - **Flaky test**: A test that passes on some runs and fails on others, with no code change.
> - **Line coverage**: The lines of code that at least one test runs.

## Why it matters

An agent that writes tests leaves them in your repository, where they guard every later change. A
test that fails one run in five, or adds nothing the suite did not already check, costs review time
and gives no signal. Meta's TestGen-LLM faced this at scale: a model proposes tests for Instagram and
Facebook code, and a pipeline decides which ones an engineer ever sees. The course's five test
filters start from its design.

## Three key ideas

1. **Filter in order of cost.** TestGen-LLM keeps a test only after "a series of progressively
   demanding semantic filters": it must build, then pass, then add coverage. A test is dropped at the
   first filter it fails, so the slow checks run only on tests that already passed the fast ones.

2. **Most candidates fail, so the filter is the product.** A trial counts only "if the generated test
   case builds, passes, and increases coverage over all existing test cases." Across its evaluation,
   most candidate tests failed at least one filter. Without the filters, an engineer would review
   mostly useless tests.

3. **Passing means passing every time.** "a test that does not pass on every one of five executions
   is deemed flaky." Existing tests are never touched, "thereby guaranteeing there will be no
   regression, by construction." The engineer keeps the final say: the tool "leaves the software
   engineer in ultimate control of the code that lands into the code base."

The course runs the three filters and adds two of its own. A coding agent in a test phase can edit
the code under test, or mock the function it claims to test. So filter 4 checks for real assertions
with no mocking of the code under test, and filter 5 checks that no source file changed. The paper
does not state either one.

One limit carries over from the paper: a test that fails is discarded, because the current code is
treated as correct. In the captured Section 4 demo run, that is how a correct test was lost.

## Apply it to your repo

1. Take the tests your agent wrote last week. Run each new test file five times in a row. Any test
   that fails once is flaky; fix it or delete it.
2. Measure what each new test adds over the existing suite, with your coverage tool's per-test or
   diff view. A test that adds no line and checks nothing new is a candidate to delete.
3. Order your own checks like the paper: collect, run, repeat, then measure. Do not compute coverage
   for a test that does not pass.
4. Read every discard reason before you delete a failing test. If the test matches the spec and the
   code does not, you found a bug, not a bad test.
5. Try it on one module: `uv run shipharness testgen --help` lists the options, and each run prints
   one reason per discarded test.
