"""
JSpeech Grammar Format module for Python
'The JSpeech Grammar Format (JSGF) is a platform-independent,vendor-independent
textual representation of grammars for use in speech recognition. Grammars are
used by speech recognizers to determine what the recognizer should listen for,
and so describe the utterances a user may say. JSGF adopts the style and
conventions of the JavaTM Programming Language in addition to use of
traditional grammar notations.'
See the specification here: https://www.w3.org/TR/jsgf/

This module supports compiling JSGF grammars using custom rules, imports and
expansions, such as the Kleene Star, optional and required groupings.
"""

from .expansions import AlternativeSet
from .expansions import Expansion
from .expansions import ExpansionError
from .expansions import filter_expansion
from .expansions import flat_map_expansion
from .expansions import KleeneStar
from .expansions import Literal
from .expansions import map_expansion
from .expansions import OptionalGrouping
from .expansions import restore_current_matches
from .expansions import Repeat
from .expansions import RequiredGrouping
from .expansions import RuleRef
from .expansions import save_current_matches
from .expansions import Sequence
from .expansions import SingleChildExpansion
from .expansions import TraversalOrder
from .expansions import VariableChildExpansion

from .grammars import Grammar
from .grammars import GrammarError
from .grammars import Import
from .grammars import RootGrammar

from .rules import HiddenRule
from .rules import PublicRule
from .rules import Rule
