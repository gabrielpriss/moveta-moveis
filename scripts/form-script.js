  // ── Formulário de orçamento (variante /form/ do teste A/B) ──
  // O ponto do teste: nesta página a conversão só dispara quando alguém
  // TERMINA o formulário. Na página do WhatsApp ela dispara no clique, e é
  // isso que inflava o relatório (50 conversões contra 18 contatos reais,
  // reunião de 25/09). Aqui o número do Google passa a ser o número real.
  (function () {
    var form = document.getElementById('orcamento-form');
    if (!form) return;

    // ── Planilha ──────────────────────────────────────────────
    // Cole aqui a URL do Web App do Apps Script (docs/formulario/).
    // Enquanto estiver vazio o formulário funciona normalmente: mede a
    // conversão e leva para o WhatsApp, só não grava na planilha.
    var ENDPOINT_PLANILHA = '';

    var etapas   = form.querySelectorAll('.f-etapa');
    var pontos   = document.querySelectorAll('.f-ponto');
    var sucesso  = document.getElementById('f-sucesso');
    var rodape   = document.getElementById('f-passo');
    var btnVolta = document.getElementById('f-voltar');
    var gradeAmb = document.getElementById('f-ambientes');
    var inputNome= document.getElementById('f-nome');
    var inputTel = document.getElementById('f-tel');
    var erroNome = document.getElementById('f-erro-nome');
    var erroTel  = document.getElementById('f-erro-tel');
    var btnEnviar= document.getElementById('f-enviar');
    var linkZap  = document.getElementById('f-link-zap');

    var etapa = 1;
    var resposta = { perfil: '', ambiente: '', prazo: '', origem: 'Formulário' };

    function mostrarEtapa(n) {
      etapa = n;
      etapas.forEach(function (el) { el.hidden = Number(el.dataset.etapa) !== n; });
      pontos.forEach(function (p) {
        var i = Number(p.dataset.progresso);
        p.classList.toggle('is-atual', i === n);
        p.classList.toggle('is-feito', i < n);
      });
      rodape.textContent = 'Etapa ' + n + ' de 4';
      btnVolta.classList.toggle('invisible', n === 1);
      if (n === 4) setTimeout(function () { inputNome.focus(); }, 80);
    }

    function montarAmbientes() {
      gradeAmb.innerHTML = '';
      (AMBIENTES[resposta.perfil] || []).forEach(function (nome) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'opcao-btn border-2 border-carvao/15 rounded-xl px-3 py-3.5 text-sm font-medium text-center';
        b.textContent = nome;
        b.dataset.campo = 'ambiente';
        b.dataset.valor = nome;
        gradeAmb.appendChild(b);
      });
    }

    // ── Entrada pelos CTAs ──────────────────────────────────────
    // Todo CTA da página é uma âncora para #formulario. Os cards já sabem o
    // perfil e o ambiente, então pulam as etapas que eles mesmos respondem:
    // quem clica em "Cozinha" não precisa responder de novo que é para casa.
    document.addEventListener('click', function (e) {
      var gatilho = e.target.closest('a[href="#formulario"], .js-ir-formulario');
      if (!gatilho) return;
      if (sucesso && !sucesso.hidden) return; // já enviou, não reinicia

      resposta.origem   = gatilho.dataset.origem || 'Formulário';
      resposta.perfil   = gatilho.dataset.perfil === 'casa'    ? 'Minha casa'
                        : gatilho.dataset.perfil === 'empresa' ? 'Minha empresa'
                        : '';
      resposta.ambiente = gatilho.dataset.ambiente || '';
      resposta.prazo    = '';

      if (resposta.perfil && resposta.ambiente) { montarAmbientes(); mostrarEtapa(3); }
      else if (resposta.perfil)                 { montarAmbientes(); mostrarEtapa(2); }
      else                                       { mostrarEtapa(1); }

      evento('abriu_formulario', { cta_origem: resposta.origem });
    });

    btnVolta.addEventListener('click', function () {
      if (etapa > 1) mostrarEtapa(etapa - 1);
    });

    form.addEventListener('click', function (e) {
      var opcao = e.target.closest('.opcao-btn');
      if (!opcao) return;
      resposta[opcao.dataset.campo] = opcao.dataset.valor;

      if (opcao.dataset.campo === 'perfil')        { montarAmbientes(); mostrarEtapa(2); }
      else if (opcao.dataset.campo === 'ambiente') { mostrarEtapa(3); }
      else if (opcao.dataset.campo === 'prazo')    { mostrarEtapa(4); }
    });

    // ── Telefone ────────────────────────────────────────────────
    // Formata (41) 99999-9999. O DDI 55, se a pessoa digitar, é removido:
    // ele já entra fixo no link do wa.me e duplicaria o prefixo.
    function formatarTel(bruto) {
      var d = String(bruto || '').replace(/\D/g, '');
      if (d.length > 11 && d.slice(0, 2) === '55') d = d.slice(2);
      d = d.slice(0, 11);
      if (d.length <= 10) return d.replace(/^(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
      return d.replace(/^(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
    }

    inputTel.addEventListener('input', function () {
      inputTel.value = formatarTel(inputTel.value);
      erroTel.classList.add('hidden');
    });
    inputNome.addEventListener('input', function () { erroNome.classList.add('hidden'); });

    // ── Envio ───────────────────────────────────────────────────
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var nome = inputNome.value.trim();
      var digitos = inputTel.value.replace(/\D/g, '');

      erroNome.classList.toggle('hidden', nome.length >= 2);
      erroTel.classList.toggle('hidden', digitos.length >= 10);
      if (nome.length < 2) { inputNome.focus(); return; }
      if (digitos.length < 10) { inputTel.focus(); return; }

      btnEnviar.disabled = true;

      var dados = {
        nome:     nome,
        telefone: inputTel.value,
        perfil:   resposta.perfil   || 'não informado',
        ambiente: resposta.ambiente || 'não informado',
        prazo:    resposta.prazo    || 'não informado',
        origem:   resposta.origem   || 'Formulário',
        pagina:   'form',
      };

      // A conversão do teste A/B. Um envio de formulário = um lead real.
      evento('lead_formulario', {
        cta_origem:   dados.origem,
        cta_perfil:   dados.perfil,
        cta_ambiente: dados.ambiente,
        lead_prazo:   dados.prazo,
      });

      // Planilha. `no-cors` porque o Apps Script não devolve cabeçalho CORS;
      // `keepalive` para o envio sobreviver ao redirecionamento logo abaixo.
      if (ENDPOINT_PLANILHA) {
        try {
          fetch(ENDPOINT_PLANILHA, {
            method: 'POST',
            mode: 'no-cors',
            keepalive: true,
            headers: { 'Content-Type': 'text/plain;charset=utf-8' },
            body: JSON.stringify(dados),
          }).catch(function () {});
        } catch (err) { /* sem planilha o lead não se perde: já foi medido */ }
      }

      var linhas = [
        'Olá! Sou ' + nome + ' e vim pelo site da Movetá.',
        '',
        'Projeto para: ' + dados.perfil,
        'Ambiente: ' + dados.ambiente,
        'Pretendo começar: ' + dados.prazo,
        'Meu WhatsApp: ' + dados.telefone,
      ];
      var url = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(linhas.join('\n'));

      // A confirmação aparece ANTES do redirecionamento de propósito: se o
      // navegador bloquear a ida automática, a pessoa ainda tem o botão, e
      // o lead já está medido e na planilha de qualquer jeito.
      form.hidden = true;
      sucesso.hidden = false;
      linkZap.href = url;
      btnVolta.classList.add('invisible');
      rodape.textContent = 'Pedido enviado';
      pontos.forEach(function (p) { p.classList.add('is-feito'); p.classList.remove('is-atual'); });
      sucesso.scrollIntoView({ block: 'center', behavior: 'smooth' });

      setTimeout(function () { window.location.href = url; }, 1200);
    });

    mostrarEtapa(1);
  })();
