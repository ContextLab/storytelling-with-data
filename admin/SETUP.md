# Maintaining and updating course materials

## Docker
- Build docker image: `docker build -t swd .`
- Get list of docker images and IDs: `docker images`
- Tag release: `docker tag <IMAGE ID> contextlab/storytelling-with-data:<TAG>`, where:
  - <IMAGE ID> is the IMAGE ID of `swd/latest`
  - <TAG> is something like `v0.5` (e.g. a version number)
- Push image to DockerHub: `docker push contextlab/storytelling-with-data`

## Helm
- Modify `config.yaml`
- Re-build pods: `helm upgrade --install jhub jupyterhub/jupyterhub --namespace jhub --version=0.8.0 --values config.yaml --recreate-pods`

### Generate Certificate Authority
- Find IP address of Kubernetes master: `kubectl cluster-info`
- Generate certificate ([source](https://github.com/helm/helm/blob/master/docs/tiller_ssl.md)):
```
openssl genrsa -out ./ca.key.pem 4096
openssl req -key ca.key.pem -new -x509 -days 7300 -sha256 -out ca.cert.pem -extensions v3_ca
```
  - note: the following needs to be added to `/etc/ssl/openssl.cnf` ([source](https://github.com/jetstack/cert-manager/issues/279)):
  ```
  [ v3_ca ]
  basicConstraints = critical,CA:TRUE
  subjectKeyIdentifier = hash
  authorityKeyIdentifier = keyid:always,issuer:always
  ```
  - Country Name: US
  - State or Province Name: New Hampshire
  - Locality Name: Hanover
  - Organization Name: Contextual Dynamics Laboratory
  - Organizational Unit Name: <BLANK>
  - Common Name: (IP address of Kubernetes master, excluding https// part)
  - Email Address: contextualdynamics@gmail.com
```
openssl genrsa -out ./helm.key.pem 4096
openssl req -key helm.key.pem -new -sha256 -out helm.csr.pem
```
  - Country Name: US
  - State or Province Name: New Hampshire
  - Locality Name: Hanover
  - Organization Name: Contextual Dynamics Laboratory
  - Organizational Unit Name: <BLANK>
  - Common Name: helm
  - Email Address: contextualdynamics@gmail.com
  - A challenge password: <REMEMBER>
```
openssl genrsa -out ./tiller.key.pem 4096
openssl req -key tiller.key.pem -new -sha256 -out tiller.csr.pem
```
  - Country Name: US
  - State or Province Name: New Hampshire
  - Locality Name: Hanover
  - Organization Name: Contextual Dynamics Laboratory
  - Organizational Unit Name: <BLANK>
  - Common Name: tiller
  - Email Address: contextualdynamics@gmail.com
  - A challenge password: <REMEMBER>
- Sign certificates:
```
openssl x509 -req -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial -in tiller.csr.pem -out tiller.cert.pem -days 730
openssl x509 -req -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial -in helm.csr.pem -out helm.cert.pem  -days 730
```
- Dry run (make sure it generates something reasonable-looking and doesn't crash):
```
helm init --dry-run --debug --tiller-tls --tiller-tls-cert ./tiller.cert.pem --tiller-tls-key ./tiller.key.pem --tiller-tls-verify --tls-ca-cert ca.cert.pem
```

### Getting certificates onto helm
- Push certificates to helm:
```
helm init --tiller-tls --tiller-tls-cert ./tiller.cert.pem --tiller-tls-key ./tiller.key.pem --tiller-tls-verify --tls-ca-cert ca.cert.pem --upgrade
```
- check deployment using `kubectl -n kube-system get deployment` (should show `tiller-deploy` in the list)
- specify IP SAN:
```
echo subjectAltName=IP:<IP address of Kubernetes master> > extfile.cnf
openssl x509 -req -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial -in tiller.csr.pem -out tiller.cert.pem -days 730 -extfile extfile.cnf
```
- Configure helm client to use client key for encryption so that we can suport TLS protection:
```
helm ls --tls --tls-ca-cert ca.cert.pem --tls-cert helm.cert.pem --tls-key helm.key.pem
```
