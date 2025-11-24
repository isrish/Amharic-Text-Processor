from amharic_text_processor.processors.html import HtmlStripper

def test_htmlstripper():
    p = HtmlStripper()
    r = p.apply("<p>ሰላም</p>")
    assert r["text"] == "ሰላም"
