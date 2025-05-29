from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import AgentInferencer

from opencompass.datasets.ThinkGeo_bench import ThinkGeoBenchDataset, ThinkGeoBenchEvaluator
from opencompass.datasets import CIBenchEvaluator

ThinkGeo_bench_reader_cfg = dict(
    input_columns=["dialogs", "resources"],
    output_column="gt_answer",
    train_split='test',
    test_split='test')

ThinkGeo_bench_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template="""{questions}""",
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=AgentInferencer, infer_mode='every_with_gt'),
)

ThinkGeo_bench_eval_cfg = dict(evaluator=dict(type=ThinkGeoBenchEvaluator, mode='every_with_gt'))

ThinkGeo_bench_datasets = [
    dict(
        abbr="ThinkGeo_bench",
        type=ThinkGeoBenchDataset,
        path="data/ThinkGeo_dataset",
        reader_cfg=ThinkGeo_bench_reader_cfg,
        infer_cfg=ThinkGeo_bench_infer_cfg,
        eval_cfg=ThinkGeo_bench_eval_cfg,
    )
]
