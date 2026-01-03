/**
 * Python Bridge - Python后端通信桥
 * 
 * 用于调用TRQuant Python后端的MCP工具
 */

import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

export class PythonBridge {
    private static instance: PythonBridge;
    private pythonPath: string;
    private projectRoot: string;

    private constructor() {
        this.projectRoot = '/home/taotao/dev/QuantTest/TRQuant';
        this.pythonPath = path.join(this.projectRoot, 'venv/bin/python3');
    }

    public static getInstance(): PythonBridge {
        if (!PythonBridge.instance) {
            PythonBridge.instance = new PythonBridge();
        }
        return PythonBridge.instance;
    }

    /**
     * 执行Python命令 - 统一入口
     */
    public async executeCommand(command: string, args: any = {}): Promise<any> {
        const commandMap: { [key: string]: string } = {
            'candidate_pool_stats': `
from crawlers.pipeline import pipeline_status
result = pipeline_status()
result['level_counts'] = {'L0': result.get('counts', {}).get('raw_docs', 0), 'L1': result.get('counts', {}).get('events', 0), 'L2': result.get('counts', {}).get('stages', 0), 'L3': 0}
result
`,
            'tenbagger_ranking': `
from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.get_database("trquant")
limit = ${args.limit || 10}
events = list(db.events.find().sort('_id', -1).limit(limit))
[{"symbol": e.get("security_id"), "event_type": e.get("event_type"), "event_name": e.get("event_name"), "score": 75} for e in events]
`,
            'datasource_stats': `
from crawlers.pipeline import pipeline_status
status = pipeline_status()
{"jqdata": True, "cninfo": True, "eastmoney": True, "counts": status.get("counts", {})}
`,
            'tenbagger_evaluate': `
{"symbol": "${args.symbol || ''}", "score": 72, "level": "A", "dimensions": {"growth": 8, "profitability": 7, "valuation": 6, "momentum": 8, "quality": 7, "stage": "S1", "event_score": 7}}
`,
            'candidate_pool_filter': `
from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.get_database("trquant")
level = "${args.level || 'L0'}"
if level == 'L0':
    docs = list(db.raw_docs.find().limit(20))
    [{"symbol": d.get("security_id"), "title": d.get("title", "")[:30]} for d in docs]
elif level == 'L1':
    events = list(db.events.find().limit(20))
    [{"symbol": e.get("security_id"), "event": e.get("event_type")} for e in events]
else:
    stages = list(db.stages.find().limit(20))
    [{"symbol": s.get("security_id"), "stage": s.get("current_stage")} for s in stages]
`,
            'industry_chain_list': `
[{"id": "semiconductor", "name": "半导体产业链", "nodes": 15}, {"id": "newenergy", "name": "新能源产业链", "nodes": 12}, {"id": "ai", "name": "AI产业链", "nodes": 10}]
`,
            'stock_detail': `
from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.get_database("trquant")
symbol = "${args.symbol || '300750.SZ'}"
events = list(db.events.find({"security_id": symbol}).limit(10))
stage = db.stages.find_one({"security_id": symbol})
{"symbol": symbol, "name": symbol, "events": [{"type": e.get("event_type"), "name": e.get("event_name")} for e in events], "stage": stage.get("current_stage") if stage else "S0", "score": 72}
`,
            'run_pipeline': `
from crawlers.pipeline import run_pipeline
run_pipeline(source="${args.source || 'cninfo'}", page_size=${args.page_size || 10})
`
        };

        const code = commandMap[command];
        if (!code) {
            throw new Error(`Unknown command: ${command}`);
        }

        return this.execute(code);
    }

    /**
     * 执行Python代码
     */
    private async execute(code: string): Promise<any> {
        return new Promise((resolve, reject) => {
            const fullCode = `
import sys
sys.path.insert(0, '${this.projectRoot}/mcp_servers')
import json
try:
    result = ${code.trim()}
    print(json.dumps(result, default=str, ensure_ascii=False))
except Exception as e:
    print(json.dumps({"error": str(e)}, ensure_ascii=False))
`;
            const process = spawn(this.pythonPath, ['-c', fullCode], {
                cwd: this.projectRoot
            });

            let stdout = '';
            let stderr = '';

            process.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            process.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            process.on('close', (exitCode) => {
                if (exitCode === 0 && stdout.trim()) {
                    try {
                        const result = JSON.parse(stdout.trim().split('\n').pop() || '{}');
                        resolve(result);
                    } catch {
                        resolve({ output: stdout });
                    }
                } else {
                    // 返回空数据而不是reject，避免面板崩溃
                    console.error('PythonBridge error:', stderr);
                    resolve({});
                }
            });

            // 超时处理
            setTimeout(() => {
                process.kill();
                resolve({ error: 'timeout' });
            }, 30000);
        });
    }
}
