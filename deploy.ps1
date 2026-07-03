$namespace = "notes-api"

kubectl apply -f k8s/ -n $namespace

kubectl rollout restart deployment/notes-api -n $namespace

kubectl rollout status deployment/notes-api -n $namespace

Write-Host ""
Write-Host "Pods:"
kubectl get pods -n $namespace

Write-Host ""
Write-Host "Services:"
kubectl get svc -n $namespace

Write-Host ""
Write-Host "Deployment completed successfully!"