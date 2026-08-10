#!/usr/bin/env node
/**
 * Gera os placeholders SVG da LP.
 *
 * Cada arquivo nasce com o nome definitivo do asset. Quando as fotos reais
 * chegarem: salve o .webp com o mesmo nome-base em public/assets/ e troque a
 * extensao no index.html (procure por `.svg" ` dentro das tags <img>).
 *
 *   node scripts/gerar-placeholders.js
 */

const fs = require('fs');
const path = require('path');

const DESTINO = path.join(__dirname, '..', 'public', 'assets');

// Cores alinhadas a identidade da logo (dourado sobre carvao)
const AREIA = '#EDE7DB';
const BRONZE = '#C9A24B';
const GRAFITE = '#211D1A';

/** Placeholder de foto: moldura em areia, moldura tracejada e legenda. */
function foto(largura, altura, rotulo) {
  const cx = largura / 2;
  const corpo = Math.max(13, Math.round(largura / 34));
  const legenda = Math.max(11, Math.round(largura / 46));
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${largura}" height="${altura}" viewBox="0 0 ${largura} ${altura}" role="img" aria-label="${rotulo}">
  <rect width="${largura}" height="${altura}" fill="${AREIA}"/>
  <rect x="12" y="12" width="${largura - 24}" height="${altura - 24}" fill="none" stroke="${BRONZE}" stroke-width="2" stroke-dasharray="10 8" opacity=".55"/>
  <g fill="none" stroke="${BRONZE}" stroke-width="2.5" opacity=".7" transform="translate(${cx - 22} ${altura / 2 - 44})">
    <rect x="0" y="0" width="44" height="34" rx="3"/>
    <circle cx="32" cy="9" r="4"/>
    <path d="M0 26l13-12 10 9 8-6 13 11"/>
  </g>
  <text x="${cx}" y="${altura / 2 + 8}" font-family="Georgia, serif" font-size="${corpo}" fill="${GRAFITE}" text-anchor="middle">${rotulo}</text>
  <text x="${cx}" y="${altura / 2 + 8 + corpo + 6}" font-family="system-ui, sans-serif" font-size="${legenda}" fill="${GRAFITE}" opacity=".55" text-anchor="middle">substituir por foto real · ${largura}x${altura}</text>
</svg>`;
}

/** Amostra de acabamento: bloco de cor com veio sutil e nome. */
function acabamento(cor, nome, tipo) {
  const claro = ['#EFE7DA', '#D8C9AE'].includes(cor);
  const texto = claro ? GRAFITE : '#FFFFFF';
  return `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400" role="img" aria-label="${nome}">
  <rect width="400" height="400" fill="${cor}"/>
  <g stroke="#000" stroke-width="1" opacity=".07">
    ${Array.from({ length: 9 }, (_, i) => `<path d="M0 ${20 + i * 45}q100 ${i % 2 ? 14 : -14} 200 0t200 0"/>`).join('\n    ')}
  </g>
  <rect x="0" y="316" width="400" height="84" fill="#000" opacity=".28"/>
  <text x="24" y="352" font-family="Georgia, serif" font-size="25" fill="${texto}">${nome}</text>
  <text x="24" y="378" font-family="system-ui, sans-serif" font-size="15" fill="${texto}" opacity=".8">${tipo}</text>
</svg>`;
}

/** Avatar circular com iniciais, para os depoimentos. */
function avatar(iniciais) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120" role="img" aria-label="Foto de ${iniciais}">
  <circle cx="60" cy="60" r="60" fill="${BRONZE}"/>
  <text x="60" y="60" font-family="Georgia, serif" font-size="42" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">${iniciais}</text>
</svg>`;
}

// A logo NAO e gerada aqui: assets/logo-moveta.png sai de
// scripts/preparar-logo.py, a partir da arte oficial em arte-original/.

const ARQUIVOS = {
  // Hero
  'hero-principal.svg': foto(1280, 860, 'Cozinha planejada: foto principal'),
  'hero-detalhe-1.svg': foto(600, 800, 'Detalhe de marcenaria'),
  'hero-detalhe-2.svg': foto(600, 400, 'Ambiente integrado'),

  // Residencial: 1 foto por PROJETO DIFERENTE (nao varias do mesmo movel)
  'residencial-cozinha.svg': foto(800, 1000, 'Cozinha planejada'),
  'residencial-dormitorio.svg': foto(800, 1000, 'Dormitório / guarda-roupa'),
  'residencial-painel-tv.svg': foto(800, 1000, 'Painel de TV para sala'),
  'residencial-lavanderia.svg': foto(800, 1000, 'Lavanderia planejada'),
  'residencial-home-office.svg': foto(800, 1000, 'Home office'),

  // Empresas: servico nivel 1 do cliente (escritorio). Somente servicos
  // citados na reuniao: moveis para escritorio, armarios/divisorias,
  // mesa de reuniao e painel para TV (21:38 e 52:16).
  'empresa-escritorio.svg': foto(800, 1000, 'Móveis para escritório'),
  'empresa-painel-tv.svg': foto(800, 1000, 'Painel para TV'),
  'empresa-armarios.svg': foto(800, 1000, 'Armários e divisórias para equipe'),
  'empresa-sala-reuniao.svg': foto(800, 1000, 'Mesa de sala de reunião'),

  // Processo / sobre / marcenaria
  'processo-medicao.svg': foto(1000, 750, 'Medição no local do cliente'),
  'processo-apresentacao.svg': foto(1000, 750, 'Apresentação do projeto ao cliente'),
  'sobre-equipe.svg': foto(800, 1000, 'Sócios: comercial e marcenaria'),
  'marcenaria-01.svg': foto(700, 500, 'Marcenaria: corte e usinagem'),
  'marcenaria-02.svg': foto(700, 500, 'Marcenaria: montagem'),
  'marcenaria-03.svg': foto(700, 500, 'Montagem na casa do cliente'),

  // Acabamentos
  'acabamento-verde-jade.svg': acabamento('#2F4F45', 'Verde Jade', 'MDF'),
  'acabamento-pau-ferro.svg': acabamento('#5C3A26', 'Pau Ferro', 'Lâmina natural'),
  'acabamento-azul-royal.svg': acabamento('#1F3B63', 'Azul Royal', 'MDF'),
  'acabamento-bege.svg': acabamento('#D8C9AE', 'Bege', 'MDF'),
  'acabamento-carvalho.svg': acabamento('#A8783F', 'Carvalho Natural', 'Lâmina natural'),
  'acabamento-off-white.svg': acabamento('#EFE7DA', 'Off White', 'MDF'),

  // Avatares dos depoimentos
  'avatar-01.svg': avatar('AC'),
  'avatar-02.svg': avatar('RM'),
  'avatar-03.svg': avatar('JP'),
  'avatar-04.svg': avatar('LF'),
};

fs.mkdirSync(DESTINO, { recursive: true });
for (const [nome, conteudo] of Object.entries(ARQUIVOS)) {
  fs.writeFileSync(path.join(DESTINO, nome), conteudo);
}
console.log(`${Object.keys(ARQUIVOS).length} placeholders gerados em public/assets/`);
