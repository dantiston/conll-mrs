#!/usr/bin/env python3

"""
Reading MRS
  load_mrs_iter(conll: Conll) -> list[MRS]
  load_mrs(sentence: Sentence) -> MRS
Saving MRS
  dump_to_conll(conll: Conll, mrs: list[MRS]) -> Conll
  dump_to_sentence(sentence: Sentence, mrs: MRS) -> Sentence
Generating MRS
  parse(utterance: str) -> Sentence
  process(conll: Conll) -> Conll
  process_sentence(sentence: Sentence) -> Sentence
"""

import itertools

from typing import Iterable, Optional, Sequence

from delphin import ace, dmrs
from delphin.interface import Response, Result
from delphin.dmrs import DMRS, Node
from delphin.mrs import MRS
from delphin.tokens import YYToken
from pyconll.unit import conll, sentence
from pyconll.util import COLUMNS_SPECIFIER


BASE_COLUMNS = ('id', 'token', 'lemma', 'upos')
MRS_COLUMNS = ('mrs:pred', 'mrs:roles', 'mrs:lnk', 'mrs:feats')
TARGET_COLUMNS = BASE_COLUMNS + MRS_COLUMNS
MRS_COLUMN_SPEC = util.format_columns_spec(TARGET_COLUMNS)


def load_mrs_iter(
    sentences: Iterable[Sentence],
    mrs_namespace_label="mrs",
    mrs_pred_label="pred",
    mrs_roles="roles",
    mrs_lnk="link",
    mrs_feats="feats",
) -> list[MRS]:
    """
    Given an Iterable of Sentence objects (such as a Conll object), return the MRS
    for each Sentence as an MRS object
    """
    return [
        load_mrs(
            sentence,
            mrs_namespace_label=mrs_namespace_label,
            mrs_pred_label=mrs_pred_label,
            mrs_roles=mrs_roles,
            mrs_lnk=mrs_lnk,
            mrs_feats=mrs_feats,
        )
        for sentence in sentences
    ]


def load_mrs(
    sentence: Sentence,
    mrs_namespace_label="mrs",
    mrs_pred_label="pred",
    mrs_roles="roles",
    mrs_lnk="link",
    mrs_feats="feats",
) -> MRS:
    """
    Given a Sentence object, return the MRS as an MRS object
    """
    pass


def dump_to_conll(conll: Conll, mrs_seq: Sequence[MRS]) -> Conll:
    """
    Given a Conll object and a list of MRS, write each MRS into the Sentence objects
    """
    if len(conll) != len(mrs_seq):
        raise Exception("Number of MRS does not match the number of sentences")
    result = Conll(conll, columns=conll._columns)
    for i, mrs in enumerate(mrs_seq):
        sentence = dump_to_sentence(conll[i], mrs)
        conll[i] = sentence
    return result


def dump_to_sentence(sentence: Sentence, mrs: MRS) -> Sentence:
    """
    Given a Sentence object and an MRS, write the MRS into the Sentence objects
    """
    pass


def parse(
    grm: str,
    utterance: str,
    mrs_namespace_label="mrs",
    mrs_pred_label="pred",
    mrs_roles="roles",
    mrs_lnk="link",
    mrs_feats="feats",
) -> Sentence:
    """
    Given an utterance, construct a Sentence object from the grammar's analysis
    """
    response = ace.parse(grm, utterance)
    return _construct_sentence(
        utterance,
        response,
        mrs_namespace_label=mrs_namespace_label,
        mrs_pred_label=mrs_pred_label,
        mrs_roles=mrs_roles,
        mrs_lnk=mrs_lnk,
        mrs_feats=mrs_feats,
    )


def parse_iter(
    grm: str,
    utterances: Iterable[str],
    mrs_namespace_label="mrs",
    mrs_pred_label="pred",
    mrs_roles="roles",
    mrs_lnk="link",
    mrs_feats="feats",
) -> Conll:
    """
    Given an iterable of utterances, construct a Conll object from the grammar's analyses
    """
    # TODO: Refactor to only open the grammar once
    return Conll(
        parse(
            grm,
            utterance,
            mrs_namespace_label=mrs_namespace_label,
            mrs_pred_label=mrs_pred_label,
            mrs_roles=mrs_roles,
            mrs_lnk=mrs_lnk,
            mrs_feats=mrs_feats,
        )
        for utterance in utterances
    )


def _construct_sentence(
    utterance: str,
    response: Response,
    mrs_namespace_label="mrs",
    mrs_pred_label="pred",
    mrs_roles="roles",
    mrs_lnk="link",
    mrs_feats="feats",
) -> Sentence:
    """
    Given an utterance and MRS, create a new Sentence object
    """
    result = _select_parse(response)
    mrs = result.mrs()
    dmrs = dmrs.from_mrs(mrs)
    nodes_by_start = _get_nodes_by_start(dmrs)
    tokens = response.tokens()
    # TODO: Refactor pyconll to allow more efficient creation
    token_strings = (_construct_token(token, i, result, mrs, dmrs, nodes_by_start[token.lnk[0]]) for i, token in enumerate(tokens))
    tmp_string = "\n".join([MRS_COLUMN_SPEC, '\n'.join(token_strings)])
    return Sentence(tmp_string, columns=TARGET_COLUMNS)


def _construct_token(
    token: YYToken,
    idx: int,
    result: Result,
    # mrs: MRS,
    dmrs: DMRS,
    # nodes_by_start: dict[int, list[tuple[int, Node]]],
    node: Node,
) -> str:
    """
    Returns string in the form of:

    id	token	lemma	upos	mrs:pred	mrs:roles	mrs:lnk	mrs:feats
    """
    return '\t'.join(
        idx, # token.id???
        token.form,
        token.form, # TODO: Get lemma from MRS?
        _get_upos(token.pos[0][0]),
        node.predicate,
        # _format_roles(idx, nodes_by_start.get(token.lnk[0], None)),
        "_", # TODO: roles
        str(node.lnk),
        "_", # TODO: properties
    )


def _dmrs_sort(node: Node) -> int:
    return node.lnk.data[0]


def _get_nodes_by_start(dmrs: DMRS) -> dict[int, list[tuple[int, Node]]]:
    return {k: list(v) for k, v in itertools.groupby(sorted(dmrs.nodes, key=_dmrs_sort), key=_dmrs_sort)}


def _get_upos(pos: str) -> str:
    # TODO: fix this
    return pos


def _format_roles(idx: int, nodes: Optional[list[tuple[int, Node]]]) -> str:
    return "|".join((_format_node(*node) for node in nodes)) if nodes else '_'


def _format_node(idx: int, node: Node) -> str:
    return f"{idx}:{node}"


def _select_parse(
    response: Response,
    sentence: Sentence = None,
) -> Result:
    """
    Get the most accurate parse given existing data in a Sentence
    """
    # TODO: Implement
    return response.result(0)


def process(grm: str, conll: Conll, pos_label="upos", dep_label="dep") -> Conll:
    """
    Given a Conll object without MRS, utilize stored POS tags and dependency
    information to select the best analysis from the grammar for each Sentence
    """
    pass


def process_sentence(sentence: Sentence) -> Sentence:
    """
    Given a Sentence object without MRS, utilize stored POS tags and dependency
    information to select the best analysis from the grammar
    """
    pass
