leeroy-rerun
------------

litl's leeroy integration robot is great, but it doesn't provide a convenient
way to rerun a job without changing the source code. This tool lets you
manually trigger job reruns from the command line.

```
export LEEROY_URL=http://leeroy.yourdomain.biz
python leeroy-rerun.py https://github.com/mozilla/socorro/pull/921 https://github.com/mozilla/socorro/pull/912
```

```
python leeroy-rerun.py -L leeroy.yourdomain.biz https://github.com/mozilla/socorro/pull/921
```

wrote this as part of my ongoing investigation of
[leeroy issue 9](https://github.com/litl/leeroy/issues/9). I expect a
resolution to that issue will obsolete this tool.

there is also a bash script that may be easier to use: https://gist.github.com/4151152 (thanks @mythmon)

executed but not tested