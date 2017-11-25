# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613

from unittest import TestCase

from mock import patch

from wotw_highlighter import BlockDecorator


class BlockDecoratorTestCase(TestCase):

    def setUp(self):
        self.build_decorator()

    def wipe_decorator(self):
        del self.block_decorator

    def build_decorator(self, *args, **kwargs):
        move_patcher = patch.object(
            BlockDecorator, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(BlockDecorator, 'validate')
        validate_patcher.start()
        self.block_decorator = BlockDecorator(*args, **kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        self.addCleanup(self.wipe_decorator)


class ValidateUnitTests(BlockDecoratorTestCase):

    def test_without_highlighted_code(self):
        self.block_decorator.highlighted_blob = None
        with self.assertRaisesRegexp(ValueError, 'Nothing to decorate'):
            self.block_decorator.validate()

    def test_with_highlighted_code(self):
        self.block_decorator.highlighted_blob = 'qqq'
        self.assertIsNone(self.block_decorator.validate())


class RemoveLineNosTestCases(BlockDecoratorTestCase):

    WITH_LINENOS = '''\
<table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre> 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14</pre></div></td><td class="code"><div class="highlight"><pre><span></span><span class="p">..</span> <span class="ow">image</span><span class="p">::</span> https://badge.fury.io/py/wotw-highlighter.svg
    <span class="nc">:target:</span> <span class="nf">https://badge.fury.io/py/wotw-highlighter</span>

<span class="p">..</span> <span class="ow">image</span><span class="p">::</span> https://travis-ci.org/wizardsoftheweb/wotw-highlighter.svg?branch=master
    <span class="nc">:target:</span> <span class="nf">https://travis-ci.org/wizardsoftheweb/wotw-highlighter</span>

<span class="p">..</span> <span class="ow">image</span><span class="p">::</span> https://coveralls.io/repos/github/wizardsoftheweb/wotw-highlighter/badge.svg?branch=master
    <span class="nc">:target:</span> <span class="nf">https://coveralls.io/github/wizardsoftheweb/wotw-highlighter?branch=master</span>


<span class="gh">``wotw-highlighter``</span>
<span class="gh">==================</span>

Until <span class="s">``v1``</span>, <span class="s">``master``</span> isn&#39;t updated frequently. Check <span class="s">``dev``</span> (<span class="s">`link </span><span class="si">&lt;https://github.com/wizardsoftheweb&gt;</span><span class="s">`__</span>) or any of the named feature branches (if any are currently committed).
</pre></div>
</td></tr></table>
'''
    WITHOUT_LINENOS = '''\
<table class="highlighttable"><tr><td class="code"><div class="highlight"><pre><span></span><span class="p">..</span> <span class="ow">image</span><span class="p">::</span> https://badge.fury.io/py/wotw-highlighter.svg
    <span class="nc">:target:</span> <span class="nf">https://badge.fury.io/py/wotw-highlighter</span>

<span class="p">..</span> <span class="ow">image</span><span class="p">::</span> https://travis-ci.org/wizardsoftheweb/wotw-highlighter.svg?branch=master
    <span class="nc">:target:</span> <span class="nf">https://travis-ci.org/wizardsoftheweb/wotw-highlighter</span>

<span class="p">..</span> <span class="ow">image</span><span class="p">::</span> https://coveralls.io/repos/github/wizardsoftheweb/wotw-highlighter/badge.svg?branch=master
    <span class="nc">:target:</span> <span class="nf">https://coveralls.io/github/wizardsoftheweb/wotw-highlighter?branch=master</span>


<span class="gh">``wotw-highlighter``</span>
<span class="gh">==================</span>

Until <span class="s">``v1``</span>, <span class="s">``master``</span> isn&#39;t updated frequently. Check <span class="s">``dev``</span> (<span class="s">`link </span><span class="si">&lt;https://github.com/wizardsoftheweb&gt;</span><span class="s">`__</span>) or any of the named feature branches (if any are currently committed).
</pre></div>
</td></tr></table>
'''

    def test_remove_linenos(self):
        self.block_decorator.highlighted_blob = self.WITH_LINENOS
        self.assertNotEqual(
            self.block_decorator.highlighted_blob, self.WITHOUT_LINENOS)
        self.block_decorator.remove_linenos()
        self.assertEqual(
            self.block_decorator.highlighted_blob, self.WITHOUT_LINENOS)
