#!/usr/bin/env bash
# pre-push-check.sh — Valida e corrige compêndio antes de push
# Uso: ./pre-push-check.sh

set -e

echo "═══════════════════════════════════════════════"
echo "  Pré-push: validação completa do vault"
echo "═══════════════════════════════════════════════"

# 1. Rebuild do compêndio
echo ""
echo "▸ [1/4] Reconstruindo compêndio..."
python3 compendium_rebuild.py rebuild --staging /tmp/compendium-prepush 2>&1 | tail -1

# 2. Verificar se há mudanças (dry-run)
echo ""
echo "▸ [2/4] Comparando com compêndio atual..."
python3 compendium_rebuild.py promote --staging /tmp/compendium-prepush 2>&1 | grep -v "ERRO:" || true

# 3. Verificar mapeamentos
echo ""
echo "▸ [3/4] Verificando mapeamentos..."
CRUAS=$(grep -rl "type: M|XPHB\|type: R|XPHB\|damage_type: [A-Z]$" content/compendium/items/ 2>/dev/null || true)
if [ -n "$CRUAS" ]; then
  echo "  ⚠ Arquivos com abreviações cruas ainda existem:"
  echo "$CRUAS"
  echo "  Aplicando correção..."
  python3 compendium_rebuild.py promote --staging /tmp/compendium-prepush --apply 2>&1 | tail -1
else
  echo "  ✓ Mapeamentos OK"
fi

# 4. Build do Hugo
echo ""
echo "▸ [4/4] Build do Hugo..."
if hugo --gc --minify --quiet 2>&1; then
  echo "  ✓ Build OK"
else
  echo "  ❌ Build falhou"
  exit 1
fi

echo ""
echo "═══════════════════════════════════════════════"
echo "  ✅ Tudo pronto para push"
echo "═══════════════════════════════════════════════"
