# ---------- Production sever ------------
FROM nginx:latest as prod

COPY run_nginx.sh .

CMD ./run_nginx.sh