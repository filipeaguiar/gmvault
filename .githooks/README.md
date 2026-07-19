# Hooks versionados

Ative os hooks deste diretório após clonar o repositório:

```bash
git config core.hooksPath .githooks
```

O hook `pre-push` publica todos os arquivos do compêndio ainda marcados com
`draft: true`. Como o hook é executado depois da criação do commit, ele cancela
o primeiro push que gerar alterações; inclua-as no commit indicado e envie
novamente.
