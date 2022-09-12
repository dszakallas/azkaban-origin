<!-- Generated file. Do not edit. If you wish to add extra info provide it in _extra.gotmpl -->
# ns-control

Administrative helm chart governing clusterwise RBAC and namespaces
![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square) ![AppVersion: 1.0.0](https://img.shields.io/badge/AppVersion-1.0.0-informational?style=flat-square)

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| namespaces | object | `{}` | Namespace configuration. Key value pair of namespace name and configuration. |
| rbac | object | `{"cluster":{"roleBindings":[]},"namespace":{}}` | RBAC configuration |
| rbac.cluster.roleBindings | list | `[]` | Clusterwide role bindings. |
| rbac.namespace | object | `{}` | Map of namespaces and their role and identity configurations. |
