from graphviz import Digraph

# Criar um novo grafo direcionado
der = Digraph(format='png', engine='dot')

# Configuração geral
der.attr(rankdir='LR', size='8,5')

# Adicionar entidades (tabelas)
der.node('Notification', '''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
<TR><TD COLSPAN="2"><B>Notification</B></TD></TR>
<TR><TD>id (PK)</TD><TD>int</TD></TR>
<TR><TD>actor_id</TD><TD>genérico</TD></TR>
<TR><TD>recipient_id (FK)</TD><TD>int</TD></TR>
<TR><TD>verb</TD><TD>string</TD></TR>
<TR><TD>action_object_id</TD><TD>genérico</TD></TR>
<TR><TD>target_id</TD><TD>genérico</TD></TR>
<TR><TD>level</TD><TD>string</TD></TR>
<TR><TD>description</TD><TD>string</TD></TR>
<TR><TD>timestamp</TD><TD>datetime</TD></TR>
<TR><TD>read</TD><TD>boolean</TD></TR>
<TR><TD>deleted</TD><TD>boolean</TD></TR>
<TR><TD>emailed</TD><TD>boolean</TD></TR>
</TABLE>>''')

der.node('User', '''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
<TR><TD COLSPAN="2"><B>User</B></TD></TR>
<TR><TD>id (PK)</TD><TD>int</TD></TR>
<TR><TD>username</TD><TD>string</TD></TR>
<TR><TD>email</TD><TD>string</TD></TR>
<TR><TD>...</TD><TD>outros campos</TD></TR>
</TABLE>>''')

der.node('Actor', '''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
<TR><TD COLSPAN="2"><B>Actor</B></TD></TR>
<TR><TD>id</TD><TD>int</TD></TR>
<TR><TD>tipo</TD><TD>string</TD></TR>
<TR><TD>objeto_id</TD><TD>genérico</TD></TR>
</TABLE>>''')

der.node('Target', '''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
<TR><TD COLSPAN="2"><B>Target</B></TD></TR>
<TR><TD>id</TD><TD>int</TD></TR>
<TR><TD>tipo</TD><TD>string</TD></TR>
<TR><TD>objeto_id</TD><TD>genérico</TD></TR>
</TABLE>>''')

der.node('ActionObject', '''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
<TR><TD COLSPAN="2"><B>ActionObject</B></TD></TR>
<TR><TD>id</TD><TD>int</TD></TR>
<TR><TD>tipo</TD><TD>string</TD></TR>
<TR><TD>objeto_id</TD><TD>genérico</TD></TR>
</TABLE>>''')

# Tabela Livros
der.node('Livros', '''Livros\n
- id_livro (PK)\n
- titulo\n
- autor\n
- ano_publicacao\n
- editora\n
- isbn\n
- disponivel''')

# Tabela Emprestimos
der.node('Emprestimos', '''Emprestimos\n
- id_emprestimo (PK)\n
- id_usuario (FK)\n
- id_livro (FK)\n
- data_emprestimo\n
- data_devolucao''')


# Relacionamentos
der.edge('Notification', 'User', label='recipient_id (FK)')
der.edge('Notification', 'Actor', label='actor_id (genérico)')
der.edge('Notification', 'Target', label='target_id (genérico)')
der.edge('Notification', 'ActionObject', label='action_object_id (genérico)')

# Renderizar o grafo
file_path = 'C:/Users/tgerm/Documents/'
der.render(file_path, format='png', cleanup=True)
file_path + '.png'
