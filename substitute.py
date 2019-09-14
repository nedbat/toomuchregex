import os
import re

def substitute_variables(text, variables):
    """
    Substitute ``${VAR}`` variables in `text`.

    Variables in the text can take a number of
    shell-inspired forms::

        $VAR
        ${VAR}
        ${VAR?}         strict: an error if no VAR.
        ${VAR-miss}     defaulted: "miss" if no VAR.
        $$              just a dollar sign.

    `variables` is a dictionary of variable values.

    Returns the resulting text with values substituted.

    """
    dollar_pattern = r"""(?x)   # Verbose regex syntax
        \$                      # A dollar sign,
        (?:                     # then
            (?P<w1> \w+ ) |         # a plain word, or
            (?P<dollar> \$ ) |      # a dollar sign, or
            {                       # a {-wrapped
                (?P<w2> \w+ )           # word,
                (?:
                    (?P<strict> \? ) |      # strict or
                    -(?P<defval> [^}]* )    # defaulted
                )?                      # maybe
            }
        )
        """

    def dollar_replace(m):
        """Called for each $replacement."""
        # Get the one group that matched.
        groups = m.group('w1', 'w2', 'dollar')
        word = next(g for g in groups if g)

        if word == "$":
            return "$"
        elif word in variables:
            return variables[word]
        elif m.group('strict'):
            msg = "Variable {} is undefined: {!r}"
            raise NameError(msg.format(word, text))
        else:
            return m.group('defval')

    text = re.sub(dollar_pattern, dollar_replace, text)
    return text
