"""
Classes for compiling JSpeech Grammar Format rules
"""
from .expansions import Expansion, RuleRef


class CompilationError(Exception):
    pass


class Rule(object):
    def __init__(self, name, visible, expansion):
        """
        :type name: str
        :type visible: bool
        :param expansion:
        """
        self.name = name
        self.visible = visible
        self.expansion = expansion
        self._reference_count = 0

    @property
    def expansion(self):
        return self._expansion

    @expansion.setter
    def expansion(self, value):
        self._set_expansion(value)

    def _set_expansion(self, value):
        # Handle the object passed in as an expansion
        self._expansion = Expansion.validate(value)

    def compile(self, ignore_tags=False):
        """
        Compile this rule's expansion tree and return the result.
        Set ignore_tags to True to not include expansion tags in the result.
        :type ignore_tags: bool
        :rtype: str
        """
        expansion = self.expansion.compile(ignore_tags)
        if not expansion:  # the compiled expansion is None or ""
            return ""

        # Raise a CompilationError if there are no non-optional leaves in the
        # expansion tree
        leaves = self.expansion.leaves
        if self.expansion.is_optional or all(map(lambda l: l.is_optional, leaves)):
            raise CompilationError("nothing in the expansion tree is required to "
                                   "be spoken.")

        result = "<%s> = %s;" % (self.name, expansion)

        if self.visible:
            return "public %s" % result
        else:
            return result

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__,
                           self.expansion)

    def matches(self, speech):
        """
        Whether speech matches this rule.
        :type speech: str
        """
        # Strip whitespace at the start of 'speech' and lower it to match regex properly.
        speech = speech.lstrip().lower()
        self.expansion.reset_for_new_match()
        result = self.expansion.matches(speech)

        # Check if the rule matched completely
        return result == "" and self.expansion.current_match is not None

    @property
    def dependencies(self):
        """
        The set of rules which this rule directly and indirectly references.
        :rtype: set
        """
        def collect_referenced_rules(expansion, result):
            """
            Recursively collect every RuleRef object's Rule in an Expansion tree and every
            referenced rule in the referenced rule's Expansion tree and so on.
            :type expansion: Expansion
            :type result: set
            """
            if isinstance(expansion, RuleRef):
                if expansion.rule not in result:  # prevent cycles
                    result.add(expansion.rule)
                    collect_referenced_rules(expansion.rule.expansion, result)
            else:
                for child in expansion.children:
                    collect_referenced_rules(child, result)

            return result
        return collect_referenced_rules(self.expansion, set())

    @property
    def reference_count(self):
        return self._reference_count

    @reference_count.setter
    def reference_count(self, value):
        assert isinstance(value, int) and value >= 0
        self._reference_count = value

    def __eq__(self, other):
        return (type(self) == type(other) and self.name == other.name and
                self.expansion == other.expansion and
                self.visible == other.visible)

    def __ne__(self, other):
        return not self.__eq__(other)


class PublicRule(Rule):
    def __init__(self, name, expansion):
        super(PublicRule, self).__init__(name, True, expansion)


class HiddenRule(Rule):
    def __init__(self, name, expansion):
        super(HiddenRule, self).__init__(name, False, expansion)
