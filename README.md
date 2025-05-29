# ThinkGeo <img src="assets/logo.png" height="50">: Evaluating Tool-Augmented Agents for Remote Sensing Tasks

![](https://i.imgur.com/waxVImv.png)

<div  align="center" style="margin-top:10px;"> 
  
[Akashah Shabbir](https://github.com/AkashahS)\*, [Muhammad Akhtar Munir]()\*, [Akshay Dudhane]()\*, [Muhammad Umer Sheikh](), [Muhammad Haris Khan](), [Paolo Fraccaro](), [Juan Bernabe Moreno](), [Fahad Shahbaz Khan]() and [Salman Khan]()

**Mohamed bin Zayed University of Artificial Intelligence, IBM Research, Linköping University, Australian National University**

[![Website](https://img.shields.io/badge/Project-Website-87CEEB)](https://mbzuai-oryx.github.io/ThinkGeo/)
[![paper](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/abs)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-F9D371)](https://huggingface.co/datasets/MBZUAI/ThinkGeo)
[![GitHub stars](https://img.shields.io/github/stars/mbzuai-oryx/ThinkGeo?style=flat&color=fff359)](https://github.com/mbzuai-oryx/ThinkGeo/stargazers)
[![GitHub license](https://img.shields.io/github/license/mbzuai-oryx/ThinkGeo?color=ff8080)](https://github.com/mbzuai-oryx/ThinkGeo/blob/main/LICENSE)

<em> <sup> *Equal Contribution  </sup> </em>
<br>

</div>

---

## 📢  Latest Updates

- **May-29-2025**: 📂 ThinkGeo benchmark is released on **_HuggingFace_** [MBZUAI/ThinkGeo](https://huggingface.co/datasets/MBZUAI/ThinkGeo)
- **May-29-2025**: 📜 Technical Report of ThinkGeo paper is released [arxiv link](https://arxiv.org/abs).

## ThinkGeo Overview

ThinkGeo is a specialized benchmark designed to evaluate how language model agents handle complex remote sensing tasks through structured tool use and step-by-step reasoning. It features human-curated queries grounded in satellite and aerial imagery across diverse real-world domains such as disaster response, urban planning, and environmental monitoring. Using a ReAct-style interaction loop, ThinkGeo tests both open and closed-source LLMs on over 400 multi-step agentic tasks. The benchmark measures not only final answer correctness but also the accuracy and consistency of tool usage throughout the process. By focusing on spatially grounded, domain-specific challenges, ThinkGeo fills a critical gap left by general-purpose evaluation frameworks.

![stats](assets/data_stats.png)

## Key Features

- A dataset comprising 436 remote sensing tasks, linked with medium to high-resolution earth observation imagery across domains like urban planning, disaster response, aviation, and environmental monitoring.

- A set of 14 executable tools simulates real-world RS workflows, including modules for perception, computation, logic, and visual annotation.

- Two evaluation modes—step-by-step and end-to-end—use with detailed metrics to assess instruction adherence, argument structure, reasoning steps, and final accuracy.

- Benchmarking advanced LLMs (GPT-4o, Claude-3, Qwen-2.5, LLaMA-3) reveals ongoing challenges in multimodal reasoning and tool integration.

## Dataset Examples

The following figure presents a set of representative samples from the ThinkGeo benchmark, a comprehensive evaluation framework for geospatial tasks. Each row in the table showcases a complete interaction flow, beginning with a user query that is grounded in remote sensing (RS) imagery. Following the user query, each example demonstrates a ReAct-based execution chain—an approach that integrates reasoning and action through a combination of tool calls and logical steps. These execution chains involve the dynamic selection and use of various tools, depending on the demands of the specific query.

![samples](assets/data_samples.png)

The data samples span a wide range of application domains, underscoring the benchmark's diversity. These domains include transportation analysis, urban planning, disaster assessment and change analysis, recreational infrastructure, and environmental monitoring, highlighting multi-tool reasoning and spatial task complexity.

## Results

Evaluation results across models on the ThinkGeo benchmark are summarized in the table. The left side presents step-by-step execution metrics, while the right side reports end-to-end performance. Metrics include tool-type accuracy—categorized by Perception (P), Operation (O), and Logic (L)—as well as final answer accuracy (Ans.) and answer accuracy with image grounding (Ans_I).

![res](assets/res.png)

## 🚀 Evaluating ThinkGeo

### Prepare ThinkGeo Dataset
1. Clone this repo.
```shell
git clone https://github.com/mbzuai-oryx/ThinkGeo.git
cd ThinkGeo
```

2. Download the dataset from [Hugging face ThinkGeo](https://huggingface.co/datasets/MBZUAI/ThinkGeo).
```shell
mkdir ./opencompass/data
```
Put it under the folder ```./opencompass/data/```. The structure of files should be:
```
ThinkGeo/
├── agentlego
├── opencompass
│   ├── data
│   │   ├── ThinkGeo_dataset
│   ├── ...
├── ...
```

### Prepare Your Model
1. Download the model weights.
```shell
pip install -U huggingface_hub
# huggingface-cli download --resume-download hugging/face/repo/name --local-dir your/local/path --local-dir-use-symlinks False
huggingface-cli download --resume-download Qwen/Qwen1.5-7B-Chat --local-dir ~/models/qwen1.5-7b-chat --local-dir-use-symlinks False
```

2. Install [LMDeploy](https://github.com/InternLM/lmdeploy).
```shell
conda create -n lmdeploy python=3.10
conda activate lmdeploy
```
For CUDA 12:
```shell
pip install lmdeploy
```

3. Launch a model service.
```shell
# lmdeploy serve api_server path/to/your/model --server-port [port_number] --model-name [your_model_name]
lmdeploy serve api_server ~/models/qwen1.5-7b-chat --server-port 12580 --model-name qwen1.5-7b-chat
```
### Deploy Tools
1. Install [AgentLego](https://github.com/InternLM/agentlego).
```shell
conda create -n agentlego python=3.11.9
conda activate agentlego
cd agentlego
pip install -r requirements_all.txt
pip install agentlego
pip install -e .
mim install mmengine
mim install mmcv==2.1.0
```
Open ```~/anaconda3/envs/agentlego/lib/python3.11/site-packages/transformers/modeling_utils.py```, then set ```_supports_sdpa = False``` to ```_supports_sdpa = True``` in line 1279.

2. Deploy tools for ThinkGeo benchmark.

To use the GoogleSearch, you should first get the Serper API key from https://serper.dev . Then export this key as environment variables.

```shell
export SERPER_API_KEY='your_serper_key_for_google_search_tool'
```

Start the tool server.

```shell
agentlego-server start --port 16181 --extra ./benchmark.py  `cat benchmark_toollist.txt` --host 0.0.0.0
```
### Start Evaluation
1. Install [OpenCompass](https://github.com/open-compass/opencompass).
```shell
conda create --name opencompass python=3.10 pytorch torchvision pytorch-cuda -c nvidia -c pytorch -y
conda activate opencompass
cd agentlego
pip install -e .
cd ../opencompass
pip install -e .
```
huggingface_hub==0.25.2 (<0.26.0)
transformers==4.40.1
2. Modify the config file at ```configs/eval_ThinkGeo_bench.py``` as below.

The ip and port number of **openai_api_base** is the ip of your model service and the port number you specified when using lmdeploy.

The ip and port number of **tool_server** is the ip of your tool service and the port number you specified when using agentlego.

```python
models = [
  dict(
        abbr='qwen1.5-7b-chat',
        type=LagentAgent,
        agent_type=ReAct,
        max_turn=10,
        llm=dict(
            type=OpenAI,
            path='qwen1.5-7b-chat',
            key='EMPTY',
            openai_api_base='http://10.140.1.17:12580/v1/chat/completions',
            query_per_second=1,
            max_seq_len=4096,
            stop='<|im_end|>',
        ),
        tool_server='http://10.140.0.138:16181',
        tool_meta='data/ThinkGeo_dataset/toolmeta.json',
        batch_size=8,
    ),
]
```

If you infer and evaluate in **step-by-step** mode, you should comment out **tool_server** and enable **tool_meta** in ```configs/eval_ThinkGeo_bench.py```, and set infer mode and eval mode to **every_with_gt** in ```configs/datasets/ThinkGeo_bench.py```:
```python
models = [
  dict(
        abbr='qwen1.5-7b-chat',
        type=LagentAgent,
        agent_type=ReAct,
        max_turn=10,
        llm=dict(
            type=OpenAI,
            path='qwen1.5-7b-chat',
            key='EMPTY',
            openai_api_base='http://10.140.1.17:12580/v1/chat/completions',
            query_per_second=1,
            max_seq_len=4096,
            stop='<|im_end|>',
        ),
        # tool_server='http://10.140.0.138:16181',
        tool_meta='data/ThinkGeo_dataset/toolmeta.json',
        batch_size=8,
    ),
]
```
```python
ThinkGeo_bench_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template="""{questions}""",
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=AgentInferencer, infer_mode='every_with_gt'),
)
ThinkGeo_bench_eval_cfg = dict(evaluator=dict(type=ThinkGeoBenchEvaluator, mode='every_with_gt'))
```

If you infer and evaluate in **end-to-end** mode, you should comment out **tool_meta** and enable **tool_server** in ```configs/eval_ThinkGeo_bench.py```, and set infer mode and eval mode to **every** in ```configs/datasets/ThinkGeo_bench.py```:
```python
models = [
  dict(
        abbr='qwen1.5-7b-chat',
        type=LagentAgent,
        agent_type=ReAct,
        max_turn=10,
        llm=dict(
            type=OpenAI,
            path='qwen1.5-7b-chat',
            key='EMPTY',
            openai_api_base='http://10.140.1.17:12580/v1/chat/completions',
            query_per_second=1,
            max_seq_len=4096,
            stop='<|im_end|>',
        ),
        tool_server='http://10.140.0.138:16181',
        # tool_meta='data/ThinkGeo_dataset/toolmeta.json',
        batch_size=8,
    ),
]
```
```python
ThinkGeo_bench_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template="""{questions}""",
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=AgentInferencer, infer_mode='every'),
)
ThinkGeo_bench_eval_cfg = dict(evaluator=dict(type=ThinkGeoBenchEvaluator, mode='every'))
```

3. Infer and evaluate with OpenCompass.
```shell
# infer only
python run.py configs/eval_ThinkGeo_bench.py --max-num-workers 32 --debug --mode infer
```
```shell
# evaluate only
# srun -p llmit -q auto python run.py configs/eval_ThinkGeo_bench.py --max-num-workers 32 --debug --reuse [time_stamp_of_prediction_file] --mode eval
srun -p llmit -q auto python run.py configs/eval_ThinkGeo_bench.py --max-num-workers 32 --debug --reuse 20250616_112233 --mode eval
```
```shell
# infer and evaluate
python run.py configs/eval_ThinkGeo_bench.py -p llmit -q auto --max-num-workers 32 --debug
```

---

## 📜 Citation 

```bibtex
@article{shabbir2025ThinkGeo,
  title={ThinkGeo: Evaluating Tool-Augmented Agents for Remote Sensing Tasks}, 
  author={Akashah Shabbir, Muhammad Akhtar Munir, Akshay Dudhane, Muhammad Umer Sheikh, Muhammad Haris Khan, Paolo Fraccaro, Juan Bernabe Moreno, Fahad Shahbaz Khan and Salman Khan},
  journal={ArXiv},
  year={2025},
  url={https://arxiv.org/abs}
}
```
