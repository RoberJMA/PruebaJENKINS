apiVersion: v1
kind: Service
metadata:
  name: selenium-hub
  labels:
    app: selenium-hub
spec:
  ports:
  - port: 4444
    targetPort: 4444
    nodePort: 31351 
    name: port0
  - port: 4443
    targetPort: 4443
    nodePort: 31352 
    name: port1
  - port: 4442
    targetPort: 4442
    nodePort: 31353  
    name: port2
  selector:
    app: selenium-hub
  type: NodePort
  sessionAffinity: None
