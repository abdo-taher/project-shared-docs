# Runtime for the API gap coding agent (automation/gap/gap_dispatch.py runs the agent inside it).
# - glibc image on purpose: the agent executable is a glibc binary (needs glibc >= 2.26) and is mounted in
#   read-only at run time; it is NOT part of the image.
# - PHP 8.5.11: the backend's composer.lock pins packages that require PHP >= 8.4 (verified: PHP 8.3 cannot install it).
# - composer comes from a digest-pinned composer:2 image.
# Nothing from the owner's machine is baked in: no credentials, no keys, no copied configuration.
FROM php:8.5-cli-bookworm@sha256:819080ed413631f6ec564184dd9acd08d9425bd863b9f8b5876b5ea2147d55e7

COPY --from=composer:2@sha256:af98f42dfff7c68ba8d53c2164fd9fde1087b7d449514baa38c418b1f6bc4bac /usr/bin/composer /usr/bin/composer

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends git unzip python3 ca-certificates curl libicu-dev libzip-dev \
 && rm -rf /var/lib/apt/lists/* \
 && docker-php-ext-install -j2 bcmath intl zip \
 && for ext in pdo_sqlite bcmath intl mbstring; do php -m | grep -qix "$ext" || exit 1; done \
 && useradd --uid 1000 --create-home --home-dir /home/agent --shell /bin/bash agent 2>/dev/null || true

# The application is large (Scramble/OpenAPI generation, the test suite): the default 128M CLI limit aborts silently.
RUN printf 'memory_limit=-1\ndisplay_errors=stderr\nerror_reporting=E_ALL\n' > /usr/local/etc/php/conf.d/zz-gap-agent.ini

# Fixed, non-secret identity for commits made by the agent.
ENV GIT_AUTHOR_NAME="Capitalix gap agent" GIT_AUTHOR_EMAIL="gap-agent@users.noreply.capitalix.invalid" \
    GIT_COMMITTER_NAME="Capitalix gap agent" GIT_COMMITTER_EMAIL="gap-agent@users.noreply.capitalix.invalid" \
    COMPOSER_HOME=/tmp/composer COMPOSER_NO_INTERACTION=1
WORKDIR /work
