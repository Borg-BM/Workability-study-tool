# syntax=docker/dockerfile:1
# Frontend image: Vite production build served by nginx, which also proxies the API (see
# docker/nginx.conf) so the browser only ever talks to one origin.
FROM node:22-slim AS build
RUN npm install -g pnpm@10.34.3
WORKDIR /src
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile
COPY . .
# Empty = same origin: API calls go to /api/... on whatever host serves the page.
ENV VITE_API_BASE_URL=""
RUN pnpm build

FROM nginx:1.29-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/dist /usr/share/nginx/html
