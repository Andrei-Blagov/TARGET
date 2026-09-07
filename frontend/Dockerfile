# Production frontend → docker push andreiblagov/frontend:latest
# Multi-stage: сборка Vue, раздача через Nginx + proxy к backend

FROM node:20-bookworm-slim AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
# Пустой VITE_API_URL → браузер ходит на тот же origin, Nginx проксирует /llm на backend
ENV VITE_API_URL=
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
