### peer dependency conflict during the `npm install` process
`npm warn ERESOLVE overriding peer dependency`
- it means the dependency resolution mechanism detected a mismatch between the expected versions of dependencies specified by a package and the actual versions being installed.

##### how to resolve
```shell
npm info <package> peerDependencies; # view peer dependencies
npm install <package>; # install compatible peer dependencies
npm install --legacy-peer-deps; # force install peer dependencies

```


```shell
 => ERROR [frontend 5/6] COPY . .                                                                           21.5s 
------                                                                                                            
[+] Running 0/16] COPY . .:                                                                                       
 ⠸ Service frontend  Building                                                                              110.3s 
failed to solve: cannot replace to directory /var/lib/docker/overlay2/x6ptivu3yyft92itkfpyjjb86/merged/usr/src/app/node_modules/@aws-sdk/client-cloudfront with file     
```
- the error indicates that docker is trying to copy a file over a directory, which is allowed. This usually happens when the `node_modules` directory already exist in the Docker image and the `COPY . .` command tries to overwrite it.