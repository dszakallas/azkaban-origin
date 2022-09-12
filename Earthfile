VERSION --use-chmod 0.6

ci:
  FROM python:3.9-slim

  ARG YQ_VERSION="v4.6.1"
  ARG KUSTOMIZE_VERSION="4.5.2"
  ARG KUBECONFORM_VERSION="0.4.12"
  ARG HELM_VERSION="3.9.0"
  ARG HELM_DOCS_VERSION="1.10.0"
  ARG JSON_SCHEMA_FOR_HUMANS_VERSION="0.41.1"

  RUN set -ex \
      && apt-get update -yqq \
      && apt-get install -yqq --no-install-recommends git curl \
      && apt-get autoremove -yqq --purge \
      && apt-get clean \
      && rm -rf \
      /root/.cache/npm \
      /var/lib/apt/lists/* \
      /tmp/* \
      /var/tmp/* \
      /usr/share/man \
      /usr/share/doc \
      /usr/share/doc-base \
      && pip install --no-cache --ignore-installed pre-commit json-schema-for-humans=="${JSON_SCHEMA_FOR_HUMANS_VERSION}"

  COPY --chmod=755 (+yq/yq --VERSION $YQ_VERSION) /bin/yq
  COPY --chmod=755 (+kustomize/kustomize --VERSION $KUSTOMIZE_VERSION) /bin/kustomize
  COPY --chmod=755 (+kubeconform/kubeconform --VERSION $KUBECONFORM_VERSION) /bin/kubeconform
  COPY --chmod=755 (+helm-docs/helm-docs --VERSION $HELM_DOCS_VERSION) /bin/helm-docs
  COPY --chmod=755 (+helm/helm --VERSION $HELM_VERSION) /bin/helm

  SAVE IMAGE --push midiparse/azkaban-ci:latest

validate:
  FROM +ci
  COPY . /repo
  WORKDIR /repo
  RUN --mount=type=cache,target=/root/.cache/pre-commit \
      git init --quiet && git add --all && pre-commit run --verbose --all-files --config ./hack/pre-commit-config-all.yaml

helm:
  FROM stefanprodan/alpine-base:latest
  ARG --required VERSION
  RUN curl -sL https://get.helm.sh/helm-v${VERSION}-linux-amd64.tar.gz | \
      tar xz
  SAVE ARTIFACT linux-amd64/helm

yq:
  FROM stefanprodan/alpine-base:latest
  ARG --required VERSION
  RUN curl -sL https://github.com/mikefarah/yq/releases/download/${VERSION}/yq_linux_amd64 -o yq
  SAVE ARTIFACT yq

kustomize:
  FROM stefanprodan/alpine-base:latest
  ARG --required VERSION
  RUN kustomize_url=https://github.com/kubernetes-sigs/kustomize/releases/download && \
      curl -sL ${kustomize_url}/kustomize%2Fv${VERSION}/kustomize_v${VERSION}_linux_amd64.tar.gz | \
      tar xz
  SAVE ARTIFACT kustomize


helm-docs:
  FROM stefanprodan/alpine-base:latest
  ARG --required VERSION
  RUN curl -sL https://github.com/norwoodj/helm-docs/releases/download/v${VERSION}/helm-docs_${VERSION}_Linux_x86_64.tar.gz | \
      tar xz
  SAVE ARTIFACT helm-docs

kubeconform:
  FROM stefanprodan/alpine-base:latest
  ARG --required VERSION
  RUN curl -sL https://github.com/yannh/kubeconform/releases/download/v${VERSION}/kubeconform-linux-amd64.tar.gz | \
      tar xz
  SAVE ARTIFACT kubeconform
