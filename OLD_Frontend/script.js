// URL base da API (altere para sua hospedagem)
const API_BASE = "http://localhost:5000/api";

// Elementos do DOM
const modal = document.getElementById("modal");
const formContent = document.getElementById("form-content");
const closeBtn = document.querySelector(".close");

// Fechar modal
closeBtn.onclick = () => (modal.style.display = "none");
window.onclick = (event) => {
  if (event.target === modal) modal.style.display = "none";
};

// Carregar dados iniciais
document.addEventListener("DOMContentLoaded", () => {
  carregarDados();
});

async function carregarDados() {
  try {
    const [doadores, receptores, pets] = await Promise.all([
      fetch(`${API_BASE}/doadores`).then((r) => r.json()),
      fetch(`${API_BASE}/receptores`).then((r) => r.json()),
      fetch(`${API_BASE}/pets`).then((r) => r.json()),
    ]);

    document.getElementById("total-doadores").textContent = doadores.length;
    document.getElementById("total-receptores").textContent = receptores.length;
    document.getElementById("total-pets").textContent = pets.length;

    atualizarLista("doadores", doadores);
    atualizarLista("receptores", receptores);
    atualizarLista("pets", pets);
  } catch (error) {
    console.error("Erro ao carregar dados:", error);
  }
}

function atualizarLista(tipo, itens) {
  const lista = document.getElementById(`lista-${tipo}`);
  lista.innerHTML = "";

  itens.forEach((item) => {
    const div = document.createElement("div");
    div.className = "item";

    if (tipo === "doadores") {
      div.innerHTML = `
                <h3>${item.nome} - ${item.cidade}</h3>
                <p><strong>Itens:</strong> ${item.itens_doacao}</p>
                <p><strong>Disponível até:</strong> ${
                  item.prazo_disponibilidade
                }</p>
                <p><strong>Pode entregar:</strong> ${
                  item.pode_entregar ? "Sim" : "Não"
                }</p>
                <p><strong>Contato:</strong> ${item.telefone}</p>
            `;
    } else if (tipo === "receptores") {
      div.innerHTML = `
                <h3>${item.nome} - ${item.cidade}</h3>
                <p><strong>Pessoas na casa:</strong> ${item.qtde_pessoas}</p>
                <p><strong>Pode retirar:</strong> ${
                  item.pode_retirar ? "Sim" : "Não"
                }</p>
                <p><strong>Contato:</strong> ${item.telefone}</p>
            `;
    } else if (tipo === "pets") {
      div.innerHTML = `
                <h3>${item.nome || "Sem nome"} - ${item.especie}</h3>
                <p><strong>Situação:</strong> ${item.situacao}</p>
                <p><strong>Descrição:</strong> ${item.descricao}</p>
                <p><strong>Contato:</strong> ${item.contato}</p>
                ${
                  item.foto
                    ? `<img src="${item.foto}" alt="Foto do pet" style="max-width: 200px;">`
                    : ""
                }
            `;
    }

    lista.appendChild(div);
  });
}

function mostrarFormulario(tipo) {
  let html = "";

  if (tipo === "doador") {
    html = `
            <h2>Cadastro de Doador</h2>
            <form onsubmit="cadastrarDoador(event)">
                <div><label>CPF:</label><input type="text" name="cpf" required></div>
                <div><label>Nome:</label><input type="text" name="nome" required></div>
                <div><label>Endereço:</label><input type="text" name="endereco" required></div>
                <div><label>Número:</label><input type="text" name="numero" required></div>
                <div><label>CEP:</label><input type="text" name="cep" required></div>
                <div><label>Bairro:</label><input type="text" name="bairro" required></div>
                <div><label>Cidade:</label><input type="text" name="cidade" required></div>
                <div><label>Estado:</label><input type="text" name="estado" required></div>
                <div><label>Telefone:</label><input type="text" name="telefone" required></div>
                <div><label>WhatsApp:</label><input type="text" name="whatsapp" required></div>
                <div>
                    <label>Pode entregar:</label>
                    <select name="pode_entregar" required>
                        <option value="true">Sim</option>
                        <option value="false">Não</option>
                    </select>
                </div>
                <div><label>Itens para doação:</label><textarea name="itens_doacao" required></textarea></div>
                <div><label>Prazo de disponibilidade:</label><input type="date" name="prazo_disponibilidade" required></div>
                <button type="submit">Cadastrar</button>
            </form>
        `;
  } else if (tipo === "receptor") {
    html = `
            <h2>Cadastro de Quem Precisa de Ajuda</h2>
            <form onsubmit="cadastrarReceptor(event)">
                <div><label>CPF:</label><input type="text" name="cpf" required></div>
                <div><label>Nome:</label><input type="text" name="nome" required></div>
                <div><label>Endereço:</label><input type="text" name="endereco" required></div>
                <div><label>Número:</label><input type="text" name="numero" required></div>
                <div><label>CEP:</label><input type="text" name="cep" required></div>
                <div><label>Bairro:</label><input type="text" name="bairro" required></div>
                <div><label>Cidade:</label><input type="text" name="cidade" required></div>
                <div><label>Estado:</label><input type="text" name="estado" required></div>
                <div><label>Telefone:</label><input type="text" name="telefone" required></div>
                <div><label>WhatsApp:</label><input type="text" name="whatsapp" required></div>
                <div><label>Quantidade de pessoas na casa:</label><input type="number" name="qtde_pessoas" required></div>
                <div>
                    <label>Pode retirar:</label>
                    <select name="pode_retirar" required>
                        <option value="true">Sim</option>
                        <option value="false">Não</option>
                    </select>
                </div>
                <button type="submit">Cadastrar</button>
            </form>
        `;
  } else if (tipo === "pet") {
    html = `
            <h2>Registro de Pet</h2>
            <form onsubmit="cadastrarPet(event)">
                <div><label>Nome (se conhecido):</label><input type="text" name="nome"></div>
                <div><label>Espécie:</label><input type="text" name="especie" required></div>
                <div><label>Raça:</label><input type="text" name="raca"></div>
                <div><label>Descrição:</label><textarea name="descricao" required></textarea></div>
                <div>
                    <label>Situação:</label>
                    <select name="situacao" required>
                        <option value="achado">Achado</option>
                        <option value="perdido">Perdido</option>
                    </select>
                </div>
                <div><label>Local do encontro/perda:</label><input type="text" name="local_encontro"></div>
                <div><label>Contato:</label><input type="text" name="contato" required></div>
                <div><label>URL da foto (opcional):</label><input type="text" name="foto"></div>
                <button type="submit">Cadastrar</button>
            </form>
        `;
  }

  formContent.innerHTML = html;
  modal.style.display = "block";
}

async function cadastrarDoador(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());
  data.pode_entregar = data.pode_entregar === "true";

  try {
    const response = await fetch(`${API_BASE}/doadores`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      alert("Doador cadastrado com sucesso!");
      modal.style.display = "none";
      carregarDados();
    } else {
      const error = await response.json();
      alert("Erro: " + error.error);
    }
  } catch (error) {
    alert("Erro ao cadastrar doador");
  }
}

async function cadastrarReceptor(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());
  data.pode_retirar = data.pode_retirar === "true";
  data.qtde_pessoas = parseInt(data.qtde_pessoas);

  try {
    const response = await fetch(`${API_BASE}/receptores`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      alert("Receptor cadastrado com sucesso!");
      modal.style.display = "none";
      carregarDados();
    } else {
      const error = await response.json();
      alert("Erro: " + error.error);
    }
  } catch (error) {
    alert("Erro ao cadastrar receptor");
  }
}

async function cadastrarPet(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch(`${API_BASE}/pets`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      alert("Pet cadastrado com sucesso!");
      modal.style.display = "none";
      carregarDados();
    } else {
      const error = await response.json();
      alert("Erro: " + error.error);
    }
  } catch (error) {
    alert("Erro ao cadastrar pet");
  }
}
