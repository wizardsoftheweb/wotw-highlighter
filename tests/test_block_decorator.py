# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613

from unittest import TestCase

from mock import call, patch

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
        self.block_decorator.inline_css = False
        self.assertIsNone(self.block_decorator.validate())

    def test_with_inline_and_no_styles(self):
        self.block_decorator.highlighted_blob = 'qqq'
        self.block_decorator.inline_css = True
        self.block_decorator.highlighted_blob_styles = None
        with self.assertRaisesRegexp(ValueError, 'No styles to inline'):
            self.block_decorator.validate()

    def test_with_inline_and_styles(self):
        self.block_decorator.highlighted_blob = 'qqq'
        self.block_decorator.inline_css = True
        self.block_decorator.highlighted_blob_styles = 'qqq'
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


class CompileHeaderUnitTests(BlockDecoratorTestCase):
    DEFAULT_OPTIONS = {
        'highlighted_blob': 'qqq'
    }

    def setUp(self):
        full_options_patcher = patch.object(
            BlockDecorator,
            'full_options',
            return_value=self.DEFAULT_OPTIONS
        )
        self.mock_full_options = full_options_patcher.start()
        self.addCleanup(full_options_patcher.stop)
        self.build_decorator()

    @patch(
        'wotw_highlighter.block_decorator.BlockHeader'
    )
    def test_header_compilation(self, mock_header):
        self.block_decorator.compile_header()
        mock_header.assert_has_calls([
            call(**self.DEFAULT_OPTIONS),
            call().render_full_header()
        ])


class InsertHeaderUnitTests(BlockDecoratorTestCase):

    WITHOUT_HEADER = "<table><tr>"
    HEADER = "header"
    WITH_HEADER = "<table>header<tr>"

    def test_inserting_header(self):
        self.block_decorator.highlighted_blob = self.WITHOUT_HEADER
        self.block_decorator.header = self.HEADER
        self.assertNotEqual(
            self.block_decorator.highlighted_blob,
            self.WITH_HEADER
        )
        self.block_decorator.insert_header()
        self.assertEqual(
            self.block_decorator.highlighted_blob,
            self.WITH_HEADER
        )


class InlineAllCssUnitTests(BlockDecoratorTestCase):
    INPUT_BLOB = (
        '<div>'
        '<p>'
        'text'
        '</p>'
        '<span>'
        'markup'
        '</span>'
        '</div>'
    )
    INPUT_STYLES = (
        'div p {'
        ' color: purple'
        '}'
    )
    OUTPUT_BLOB = (
        '<div>\n'
        '<p style="color:purple">'
        'text'
        '</p>\n'
        '<span>'
        'markup'
        '</span>\n'
        '</div>'
    )

    def test_inlining(self):
        self.block_decorator.highlighted_blob = self.INPUT_BLOB
        self.block_decorator.highlighted_blob_styles = self.INPUT_STYLES
        self.assertNotEqual(
            self.block_decorator.highlighted_blob,
            self.OUTPUT_BLOB
        )
        self.block_decorator.inline_all_css()
        self.assertEqual(
            self.block_decorator.highlighted_blob,
            self.OUTPUT_BLOB
        )


class ApplyDestructiveDecorationsUnitTests(BlockDecoratorTestCase):

    @patch.object(BlockDecorator, 'inline_all_css')
    def test_without_inline(self, mock_inline):
        self.block_decorator.inline_css = False
        self.block_decorator.apply_destructive_decorations()
        self.assertFalse(mock_inline.called)

    @patch.object(BlockDecorator, 'inline_all_css')
    def test_with_inline(self, mock_inline):
        self.block_decorator.inline_css = True
        self.block_decorator.apply_destructive_decorations()
        mock_inline.called.assert_called_once_with()


class DecorateUnitTests(BlockDecoratorTestCase):

    def setUp(self):
        compile_patcher = patch.object(BlockDecorator, 'compile_header')
        self.mock_compile = compile_patcher.start()
        self.addCleanup(compile_patcher.stop)
        insert_patcher = patch.object(BlockDecorator, 'insert_header')
        self.mock_insert = insert_patcher.start()
        self.addCleanup(insert_patcher.stop)
        remove_patcher = patch.object(BlockDecorator, 'remove_linenos')
        self.mock_remove = remove_patcher.start()
        self.addCleanup(remove_patcher.stop)
        self.build_decorator()

    def test_with_everything(self):
        self.block_decorator.linenos = True
        self.block_decorator.no_header = False
        self.block_decorator.blob_path = 'some/path'
        self.block_decorator.title = 'title'
        self.block_decorator.decorate()
        self.mock_compile.assert_called_once_with()
        self.mock_insert.assert_called_once_with()
        self.assertFalse(self.mock_remove.called)

    def test_without_linenos(self):
        self.block_decorator.linenos = False
        self.block_decorator.no_header = False
        self.block_decorator.blob_path = 'some/path'
        self.block_decorator.title = 'title'
        self.block_decorator.decorate()
        self.assertFalse(self.mock_compile.called)
        self.assertFalse(self.mock_insert.called)
        self.mock_remove.assert_called_once_with()

    def test_without_header(self):
        self.block_decorator.linenos = True
        self.block_decorator.no_header = True
        self.block_decorator.blob_path = 'some/path'
        self.block_decorator.title = 'title'
        self.block_decorator.decorate()
        self.assertFalse(self.mock_compile.called)
        self.assertFalse(self.mock_insert.called)
        self.assertFalse(self.mock_remove.called)

    def test_without_any_title(self):
        self.block_decorator.linenos = True
        self.block_decorator.no_header = False
        self.block_decorator.blob_path = None
        self.block_decorator.title = None
        self.block_decorator.decorate()
        self.assertFalse(self.mock_compile.called)
        self.assertFalse(self.mock_insert.called)
        self.assertFalse(self.mock_remove.called)
