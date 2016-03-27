from semsimilar.model.document import Document
from semsimilar.model.document_worker import parallel_process
from semsimilar.textprocessor.tokenize import CodeTokenizer
import unittest


class ParallelProcessTestCase(unittest.TestCase):
    def test(self):
        expected_text = [u'tool convert visual j# code c#', u'calcul someon age c#', u'set form opac use decim doubl']
        Document.set_tokenizer(CodeTokenizer())
        posts = [{
            "Id": "4",
            "Title": "When setting a form's opacity should I use a decimal or double?",
            "Body": "<p>I want to use a track-bar to change a form's opacity.<\/p>&#xA;&#xA;<p>This is my code:<\/p>&#xA;&#xA;<pre><code>decimal trans = trackBar1.Value \/ 5000;&#xA;this.Opacity = trans;&#xA;<\/code><\/pre>&#xA;&#xA;<p>When I try to build it, I get this error:<\/p>&#xA;&#xA;<blockquote>&#xA;  <p>Cannot implicitly convert type 'decimal' to 'double'.<\/p>&#xA;<\/blockquote>&#xA;&#xA;<p>I tried making <code>trans<\/code> a <code>double<\/code>, but then the control doesn't work. This code has worked fine for me in VB.NET in the past. <\/p>&#xA;",
            "Tags": "<c#><winforms><type-conversion><opacity>"
        }, {
            "Id": "8",
            "Title": "Tool for Converting Visual J# code to C#?",
            "Body": "<p>Are there any conversion tools for porting from <strong>Visual J#<\/strong> code to <strong>C#<\/strong>?<\/p>&#xA;",
            "Tags": "<c#><code-generation><j#><visualj#>"
        }, {
            "Id": "9",
            "Title": "How do I calculate someone's age in C#?",
            "Body": "<p>Given a <code>DateTime<\/code> representing a person's birthday, how do I calculate their age?  <\/p>&#xA;",
            "Tags": "<c#><.net><datetime>"
        }]
        docs, texts = parallel_process(posts, 2)
        self.assertEqual(len(docs), 3)
        self.assertEqual(len(expected_text), len(texts))
