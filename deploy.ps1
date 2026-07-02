kubectl apply -f k8s/

kubectl rollout restart deployment notes-api

kubectl rollout status deployment notes-api

Write-Host ""
Write-Host "Pods:"
kubectl get pods

Write-Host ""
Write-Host "Services:"
kubectl get svc

Write-Host ""
Write-Host "Deployment completed successfully!"