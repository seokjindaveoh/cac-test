"""Helpers used by every cell of ep_dr_oss.ipynb: run a shell command, time a notebook step, keep a time table.

The notebook stays readable because the bookkeeping lives here:

    run = StepRunner(work=WORK, mode=MODE, train=TRAIN)
    with run.step('download MNIST', 'train'):
        run.sh('bash get_mnist.sh ...')

Every step is written to WORK/times.json right away, so the time table (last cell) also works after a crash.
A failing step does not stop the notebook: the error is printed, recorded, and the next cell can still run.
"""
import contextlib
import json
import os
import subprocess
import time
import traceback
from pathlib import Path

# Readable names for the step groups in the time table
GROUP_NAMES = {
    'setup': 'install',
    'train': 'training',
    'sim': 'simulation',
    'layout': 'layout',
    'route': 'routing',
    'verify': 'verification',
}


class StepRunner:
    def __init__(self, work, mode, train):
        self.work = Path(work)
        self.mode = mode
        self.train = train
        (self.work / 'logs').mkdir(parents=True, exist_ok=True)
        # Time records of earlier runs in the same WORK folder are kept (the table filters by mode and start time)
        self.times_file = self.work / 'times.json'
        self.times = json.loads(self.times_file.read_text()) if self.times_file.exists() else []

    def _save(self, record):
        self.times.append(record)
        self.times_file.write_text(json.dumps(self.times, indent=1, ensure_ascii=False))

    def sh(self, cmd, log=None, tail=15, cwd=None, env=None, timeout=None):
        """Run one bash command.

        - The full output goes to a log file (WORK/logs/...); only the last `tail` lines are printed.
        - A non-zero exit code raises RuntimeError, which the surrounding `step` records as a failure.
        - Returns the output as a list of lines (for checks in the notebook).
        """
        log = Path(log) if log else self.work / 'logs' / f'sh_{int(time.time() * 1000)}.log'
        full_env = dict(os.environ, **(env or {}))
        t0 = time.time()
        with open(log, 'w') as f:
            rc = subprocess.call(['bash', '-c', cmd], stdout=f, stderr=subprocess.STDOUT,
                                 cwd=cwd, env=full_env, timeout=timeout)
        lines = log.read_text(errors='ignore').splitlines()
        for line in (lines[-tail:] if tail else []):
            print('   ', line[:220])
        short = cmd[:140] + ('…' if len(cmd) > 140 else '')
        print(f'  [{time.time() - t0:.1f} s, rc={rc}] {short}')
        if rc:
            raise RuntimeError(f'rc={rc}: {cmd[:200]} (log {log})')
        return lines

    @contextlib.contextmanager
    def step(self, name, group, note=''):
        """Time one notebook step and record whether it worked.

        Use as `with run.step(...) as r:`; the cell may put a short result into r['note'] (shown in the time table).
        Exceptions inside the block are caught here, printed and recorded; the notebook goes on.
        """
        record = dict(name=name, group=group, mode=self.mode, train=self.train, note=note, start=time.time())
        print(f'■ {name} ({GROUP_NAMES.get(group, group)}) start')
        try:
            yield record
            record['ok'] = record.get('ok', True)
        except Exception as ex:
            record['ok'] = False
            record['error'] = str(ex)[:400]
            print(f'  ✗ failed: {ex}')
            traceback.print_exc(limit=1)
        record['sec'] = round(time.time() - record['start'], 1)
        self._save(record)
        status = 'ok' if record['ok'] else ('skipped' if record['ok'] is None else 'FAILED')
        print(f'■ {name}: {record["sec"]} s, {status}')

    def skip(self, name, group, why):
        """A step this mode does not run: keep the reason in the time table (0 s, 'skipped')."""
        record = dict(name=name, group=group, mode=self.mode, sec=0.0, ok=None, note=why, start=time.time())
        self._save(record)
        print(f'■ {name}: skipped — {why}')
