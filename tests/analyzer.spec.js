const assert = require("node:assert/strict");
const analyzer = require("../src/analyzer.js");

const sample = [
  "醫師：最近一週睡眠怎麼樣？",
  "患者：幾乎每天都睡不好，半夜醒來後就很難再睡。",
  "患者：一直很緊張，也很容易對家人生氣，心情很低落，覺得自己很沒用。",
  "患者：沒有想傷害自己，也沒有不想活。",
].join("\n");

const sampleResult = analyzer.analyzeTranscript(sample);
assert.equal(sampleResult.bsrs.suicide.score, 0, "negated suicide ideation should not be scored");
assert.ok(sampleResult.bsrs.total >= 8, "symptom keywords should produce a non-trivial BSRS score");
assert.ok(sampleResult.report.includes("BSRS-5 總分"));

const crisis = "患者：我最近想死，也想過用藥結束生命，這個想法非常嚴重。";
const crisisResult = analyzer.analyzeTranscript(crisis);
assert.ok(crisisResult.bsrs.suicide.score >= 3, "suicide plan language should be high risk");
assert.equal(crisisResult.bsrs.risk.key, "suicide");

const pii = "姓名：王小明\n電話：0912-345-678\n身分證：A123456789\n地址：台北市中正區仁愛路1號\nemail test@example.com";
const deid = analyzer.deidentifyTranscript(pii);
assert.ok(!deid.text.includes("王小明"));
assert.ok(!deid.text.includes("0912"));
assert.ok(!deid.text.includes("A123456789"));
assert.ok(!deid.text.includes("test@example.com"));

console.log("Analyzer checks passed.");
