###################
# BASE 
###################
FROM node:20.11.1-bullseye-slim as base

WORKDIR /app

COPY package.json ./
COPY pnpm-lock.yaml ./
COPY .npmrc ./

# Enable pnpm
RUN corepack enable

# Install dependencies
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store pnpm fetch --frozen-lockfile
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store pnpm install --frozen-lockfile

###################
# DEVELOPMENT
###################
FROM base as development

ENV NODE_ENV development

COPY . .

ENV HOST 0.0.0.0
ENV PORT 3000

EXPOSE 3000

# Start the app
CMD ["pnpm", "run", "dev"]

###################
# BUILDING
###################
FROM base as build

COPY . .

# Build the app
RUN pnpm run build

###################
# PRODUCTION
###################
FROM node:20.11.1-bullseye-slim as production

ENV NODE_ENV production

WORKDIR /app

COPY --from=build /app/.output/ ./.output/

ENV HOST 0.0.0.0
ENV PORT 3000

# Run as non-root user
USER node

CMD ["node", "./.output/server/index.mjs"]