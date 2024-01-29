#call add document
  #calls compute terms which takes in doc.text -> outputputs an array
from typing import List, Dict, Tuple

import math
import pandas as pd

import spacy
nlp = spacy.load("en_core_web_sm")

from pydantic import BaseModel, Field
from collections import Counter
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup

class Document(BaseModel):
    id: int
    text: str  # index on text

class BM25Query(BaseModel):
    phrase: str
    max_results: int = 5

class RankedDocument(BaseModel):
    document: Document
    score: float

class BM25Response(BaseModel):
    datums: List[RankedDocument] = Field(default_factory=list)

class BM25:
    def __init__(
        self,
        k1: float = 1.2,
        b: float = 0.75,
        average_doc_length_sample_size: int = int(10e4),
    ):
        self.k1 = k1
        self.b = b

        self.nlp = spacy.load("en_core_web_sm")

        self._average_doc_length_sample_size = average_doc_length_sample_size

        self._docs: pd.DataFrame = pd.DataFrame(
            columns=["doc_id", "text", "length"]
        ).set_index(["doc_id"])
        self._term_doc_associations: pd.DataFrame = pd.DataFrame(
            columns=["term", "doc_id", "count"]
        ).set_index(["term", "doc_id"])

    @property
    def _num_documents(self) -> int:
        return len(self._docs)

    def _get_num_documents_containing_term(self, term: str) -> int:
        try:
            return len(self._term_doc_associations.loc[[term]])
        except KeyError:
            return 0
        except Exception as e:
            raise RuntimeError("Failed to calculate N") from e

    def _compute_idf(self, term: str) -> float:
        N = self._num_documents
        n_qi = self._get_num_documents_containing_term(term=term)
        return math.log(1 + ((N - n_qi + 0.5) / (n_qi + 0.5)))

    def _get_doc_by_id(self, doc_id: int) -> Document:
        return Document(id=doc_id, text=self._docs.at[doc_id, "text"])

    def _compute_terms(self, document: str) -> List[str]:
        return [
            token.lemma_
            for token in self.nlp(document)
            if 1 == 1
            and not token.is_stop
            and not token.is_punct
            and not token.is_bracket
            and not token.is_quote
            and not token.is_space
        ]

    def _compute_approx_average_doc_length(self) -> float:
        if self._num_documents < self._average_doc_length_sample_size:
            return self._docs["length"].mean()

        return self._docs.sample(n=self._average_doc_length_sample_size)["length"].mean()


     # return Dict<doc_id, score>

    # Returns Tuple<doc_id, doc_length, term_count>
    def _get_relevant_doc_ids_lengths_counts(
        self, term: str
    ) -> List[Tuple[int, int, int]]:
        try:
            doc_id_term_count_df = (
                self._term_doc_associations.loc[term].reset_index()
            )
            doc_ids: List[int] = doc_id_term_count_df["doc_id"].to_list()
            doc_length = self._docs.loc[doc_ids]["length"].to_list()  # type: ignore

            return list(
                zip(doc_ids, doc_length, doc_id_term_count_df["count"].to_list())
            )
        except KeyError:
            return []
        except Exception as e:
            raise RuntimeError("failed to get relevant docs") from e

    def _compute_scores_for_relevant_docs(
        self, search_terms: List[str]
    ) -> Dict[int, float]:
        scores: Dict[int, float] = {}
        average_doc_length = self._compute_approx_average_doc_length()

        for term in search_terms:
            idf = self._compute_idf(term=term)
            docs_lengths_counts = self._get_relevant_doc_ids_lengths_counts(term=term)

            for doc_id, doc_length, term_count in docs_lengths_counts:
                incremental_score = (
                    idf
                    * (term_count * (self.k1 + 1))
                    / (
                        term_count
                        + self.k1
                        * (1 - self.b + self.b * (doc_length / average_doc_length))
                    )
                )

                scores[doc_id] = scores.get(doc_id, 0.0) + incremental_score

        return scores

    def transform_bm25_response(response: BM25Response):
        transform_response = {
            "documents": [
                {"id": datum.document.id, "text": datum.document.text}
                for datum in response.datums
            ]
        }
        return transform_response

    def search(self, query: BM25Query) -> BM25Response:
        print('search called')
        search_terms = self._compute_terms(query.phrase)
        print('search_terms', search_terms)
        scores = self._compute_scores_for_relevant_docs(search_terms=search_terms)
        print('scores', scores)
        resp = BM25Response()

        for doc_id, score in sorted(
            scores.items(), key=lambda datum: datum[1], reverse=True
        ):
            if len(resp.datums) > query.max_results:
                break
            resp.datums.append(
                RankedDocument(document=self._get_doc_by_id(doc_id=doc_id), score=score)
            )
        # print('resp', resp)
        transformed_list = [
        {"id": datum.document.id, "text": datum.document.text}
        for datum in resp.datums
        ]
        transformed_resp = {"documents": transformed_list}
        return transformed_resp
        # return resp

    def add_document(self, doc: Document):
        # print('add doc called')
        #call  compute terms -> out puts array of terms
        terms = self._compute_terms(doc.text)
        #create loc prop with id on self -> set to array of text and length of terms
        self._docs.loc[doc.id] = [doc.text, len(terms)]
        rows = []
        #loop thru terms, add to array
        for term, count in Counter(terms).items():
            rows.append({"term": term, "doc_id": doc.id, "count": count})
        #call concat doc associations to rows
        if rows:
            self._term_doc_associations = pd.concat(
                [self._term_doc_associations, pd.DataFrame(rows).set_index(["term", "doc_id"])]
            )
        # print(rows)


