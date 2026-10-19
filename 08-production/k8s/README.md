# Kubernetes manifests for the self-hosted LangGraph agent (chapter 08/03).

Apply order:

```bash
kubectl create secret generic agent-secrets \
  --from-literal=anthropic-api-key=$ANTHROPIC_API_KEY \
  --from-literal=postgres-url=$POSTGRES_URL
kubectl apply -f 08-production/k8s/
```

Notes:

- Build the image with `langgraph build` and push it to your registry;
  the old prebuilt `langchain/langgraph` base image no longer exists.
- Use a managed Postgres for the checkpointer in production; self-hosted
  Postgres on Kubernetes is for development only.
- The HPA scales on `requests_per_second`, a custom metric you must
  expose (LLM calls are I/O-bound, so CPU is the wrong signal).
