FROM ollama/ollama:latest

COPY ollama-entrypoint.sh /bin/ollama-entrypoint.sh
RUN chmod +x /bin/ollama-entrypoint.sh

ENTRYPOINT ["/bin/ollama-entrypoint.sh"]
CMD ["/bin/ollama-entrypoint.sh"]
