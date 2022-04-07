not sure what I'm gonna do with this yet but for now it can do very basic version control

```bash
$ echo "foo" > file

$ r2 -q file

$ echo "bar" >> file

$ r2 -q file

$ r2 -c file 1
foo

$ r2 -c file 2
foo
bar
```

it stores data in the same way as [rookie](https://github.com/18fadly-anthony/rookie) and [backr2](https://github.com/18fadly-anthony/backr2)
