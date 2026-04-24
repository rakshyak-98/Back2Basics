
## zip
```bash
zip -e output.zip folder/; # password protect zip.
zip -z output.zip; # add comment to zip folder.
zip -r archive.zip source_dir -x "excluded_dir/*";
```

```sh
zip -r output.zip folder_name1 folder_name2;
```
- `-r` includes sub-folders files

```sh
zip existin.zip file1 file2; # add files to existing zip.
zip -r otuput.zip folder/ -x "*.log" "*.tmp";
```
- `-x` exclude files/patterns

```sh
unzip -l output.zip; # list contents of zip file.
```

```bash
unzip -l archive.zip; # see inside .zip archive
unzip -j <file path to unzip>;
unzip -r archive.zip source_dir -x "excluded_dir/*" "**/dist/*";
```
