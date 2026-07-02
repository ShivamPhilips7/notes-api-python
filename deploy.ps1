kubectl apply -f k8s/

kubectl rollout restart deployment notes-api

kubectl rollout status deployment notes-api