# --------- Build stage ------------

FROM klakegg/hugo:0.111.3 as hugo-builder

WORKDIR /hugo/src

#RUN hugo --baseUrl="http://iscsc.fr"
#RUN hugo --destination=./build/blog

CMD ["--destination=/hugo/build/blog"]
#CMD bash
# ---------- Production sever ------------

FROM nginx:latest as prod

#WORKDIR /blog

#COPY --from=hugo-builder /hugo/public .

COPY run_nginx.sh .

CMD ./run_nginx.sh