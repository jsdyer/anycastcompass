import test from 'node:test';import assert from 'node:assert/strict';
import {switches} from '../web/model.mjs';
test('instance switches require the same probe and root and ignore unanswered samples',()=>{const base={probe:1,root:'A',asn:2};assert.equal(switches([{...base,timestamp:'2026-01-01',instance:'one'},{...base,timestamp:'2026-01-02',instance:null},{...base,timestamp:'2026-01-03',instance:'two'},{...base,probe:2,timestamp:'2026-01-04',instance:'three'}]).length,1);});
