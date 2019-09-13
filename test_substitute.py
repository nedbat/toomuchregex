import pytest
from substitute import substitute_variables

VARS = {
    'FOO': 'fooey',
    'BAR': 'xyzzy',
}

@pytest.mark.parametrize("before, after", [
    ("Nothing to do", "Nothing to do"),
    ("Dollar: $$", "Dollar: $"),
    ("Simple: $FOO is fooey", "Simple: fooey is fooey"),
    ("Braced: X${FOO}X.", "Braced: XfooeyX."),
    ("Missing: x${NOTHING}y is xy", "Missing: xy is xy"),
    ("Multiple: $$ $FOO $BAR ${FOO}", "Multiple: $ fooey xyzzy fooey"),
    ("Ill-formed: ${%5} ${{HI}} ${", "Ill-formed: ${%5} ${{HI}} ${"),
    ("Strict: ${FOO?} is there", "Strict: fooey is there"),
    ("Defaulted: ${WUT-missing}!", "Defaulted: missing!"),
    ("Defaulted empty: ${WUT-}!", "Defaulted empty: !"),
])
def test_substitute_variables(before, after):
    assert substitute_variables(before, VARS) == after

@pytest.mark.parametrize("text", [
    "Strict: ${NOTHING?} is an error",
])
def test_substitute_variables_errors(text):
    with pytest.raises(NameError) as exc_info:
        substitute_variables(text, VARS)
    assert text in str(exc_info.value)
    assert "Variable NOTHING is undefined" in str(exc_info.value)

def test_substitute():
    before = "Look: $FOO ${BAR-default} $$"
    data = {'FOO': 'Xyzzy'}
    after = substitute_variables(before, data)
    assert after == "Look: Xyzzy default $"
