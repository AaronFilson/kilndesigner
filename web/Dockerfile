# The web app: built with Vite, served by nginx, which passes /api to the API (see nginx.conf).
# Build from the repository root: `docker build -f web/Dockerfile .`

FROM node:24-alpine AS build
WORKDIR /src
COPY package.json package-lock.json tsconfig.base.json ./
COPY packages/api-client/package.json packages/api-client/
COPY web/package.json web/
RUN --mount=type=cache,target=/root/.npm npm ci
COPY packages/api-client packages/api-client
COPY web web
RUN npm run build --workspace @kilndesigner/web


FROM nginxinc/nginx-unprivileged:1.30-alpine
COPY web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/web/dist /usr/share/nginx/html
EXPOSE 8080
