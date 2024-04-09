FROM node:alpine    
EXPOSE 3000
COPY ./db.json /opt/db.json
RUN yarn global add json-server
CMD ["json-server", "-h", "0.0.0.0", "/opt/db.json"]
