"""
Module of additional macros provided by the mkdocs-macros-plugin to LEMMA's
documentation.
"""

def define_env(env):
    @env.macro
    def print_concept(concept, conceptInfo):
        """ Return printable Markdown representation of a metamodel concept. """

        kindString = kind_string(conceptInfo)
        superConceptString = super_concept_string(conceptInfo)
        if superConceptString:
            return '%s `%s` : %s' % (kindString, concept, superConceptString)
        else:
            return '%s `%s`' % (kindString, concept)

    def kind_string(conceptInfo):
        """
        Return printable Markdown representation of a metamodel kind or the
        string 'Class' if no metamodel kind was given.
        """

        if not 'kind' in conceptInfo:
            return 'Class'

        kindParts = [p.capitalize() for p in conceptInfo['kind'].split()]
        return ' '.join(kindParts)

    def super_concept_string(conceptInfo):
        """
        Return printable Markdown representation of the super concept of a
        metamodel concept.
        """

        if not 'references' in conceptInfo \
            or not 'super_concept' in conceptInfo['references']:
            return ''

        superConceptInfo = conceptInfo['references']['super_concept']
        conceptName = superConceptInfo.get('name') or ''
        externalRefUri = superConceptInfo.get('external_ref_uri') or ''
        internalRefKind = superConceptInfo.get('internal_ref_kind') or ''
        return type_ref(conceptName, conceptName, externalRefUri,
            internalRefKind)

    @env.macro
    def print_attribute(concept, attribute, attributeInfo):
        """
        Return printable Markdown representation of an attribute of a metamodel
        concept.
        """

        typeString = type_string(attributeInfo)
        parameterString = parameter_string(attributeInfo)
        attributeId = 'id="attribute-%s-%s"' % (concept, attribute)
        return '%s `%s`%s { %s }' % \
            (typeString, attribute, parameterString, attributeId)

    def type_string(typeInfo):
        """
        Return printable Markdown representation of a type including 
        multiplicity information, and internal or external reference links.
        """

        if not 'type' in typeInfo:
            return ''

        typeName = typeInfo['type'].get('name') or ''
        multiplicity = str(typeInfo['type'].get('multiplicity') or '')
        externalRefUri = typeInfo['type'].get('external_ref_uri') or ''
        internalRefKind = typeInfo['type'].get('internal_ref_kind') or ''

        typeLabel = type_name_with_multiplicity(typeName, multiplicity)
        return type_ref(typeName, typeLabel, externalRefUri, internalRefKind)

    def type_name_with_multiplicity(typeName, multiplicity):
        """
        Return printable Markdown representation of a type and its multiplicity         
        information.
        """

        if typeName and multiplicity:            
            return '%s[%s]' % (typeName, multiplicity)
        elif typeName:
            return typeName
        
        return ''

    def type_ref(typeName, typeLabel, externalRefUri, internalRefKind):
        """
        Return printable Markdown representation of an internal or external
        type reference.
        """

        if externalRefUri:
            return '[`%s`](%s)' % (typeLabel, externalRefUri)
        elif internalRefKind:
            return '[`%s`](#%s-%s)' % (typeLabel, internalRefKind, typeName)
        elif typeName:
            return '`%s`' % typeLabel

        return ''

    def parameter_string(attributeInfo):
        """
        Return printable Markdown representation of the parameter list of a
        metamodel attribute that represents a method.
        """

        attributeKind = attributeInfo.get('kind') or ''
        parameters = attributeInfo.get('parameters') or {}
        if attributeKind.lower() != 'method':
            return ''

        paramStrings = []
        for parameter, parameterInfo in parameters.items():
            typeString = type_string(parameterInfo)
            paramStrings.append('%s `%s`' % (typeString, parameter))
        return '<code>(</code>%s<code>)</code>' % ', '.join(paramStrings)
