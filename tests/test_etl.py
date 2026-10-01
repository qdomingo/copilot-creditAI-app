"""
Tests para el módulo ETL
"""
import pytest
import pandas as pd
from pathlib import Path
from src.etl.process_credits import apply_budget_increases, process_licenses_and_credits

# Placeholder para tests futuros


def test_apply_budget_increases_replaces_only_matching_aliases(tmp_path):
	users = pd.DataFrame({
		'cdalias': ['rpedra', 'other', 'zero'],
		'creditos_base': [39, 19, 19],
		'creditos_base_licencia': [39, 19, 19],
	})
	budget_file = tmp_path / 'budget.xlsx'
	pd.DataFrame({
		'User': ['rpedra_indra', 'zero_indra', 'unknown_indra'],
		'Credits Available Current Month': [157000, 0, 99900],
		'By Chat': [1, 2, 3],
	}).to_excel(budget_file, index=False)

	result = apply_budget_increases(users, str(budget_file))

	assert result['creditos_base'].tolist() == [1570, 19, 0]
	assert result['creditos_base_licencia'].tolist() == [39, 19, 19]


@pytest.mark.parametrize('with_budget', [False, True])
def test_process_licenses_and_credits_with_optional_budget(tmp_path, with_budget):
	licenses_path = tmp_path / 'licenses.xlsx'
	credits_path = tmp_path / 'credits.csv'
	output_path = tmp_path / 'processed.xlsx'
	budget_path = tmp_path / 'budget.xlsx'
	columns = ['A', 'Estado', 'Licencia', 'D', 'E', 'Proyecto', 'G',
			   'Empresa', 'I', 'Código', 'Nombre', 'Mail']
	pd.DataFrame([
		['', 'Asignada', 'Copilot Enterprise', '', '', 'P', '', 'Indra', '', 1, 'R', 'rpedra@indra.com'],
		['', 'Asignada', 'Copilot Business', '', '', 'P', '', 'Indra', '', 2, 'O', 'other@indra.com'],
	], columns=columns).to_excel(licenses_path, index=False)
	pd.DataFrame({
		'username': ['rpedra_indra', 'other_indra'],
		'quantity': [100, 200],
		'unit_type': ['ai-credits', 'ai-credits'],
		'date': ['2026-10-01', '2026-10-01'],
	}).to_csv(credits_path, index=False)
	pd.DataFrame({
		'User': ['rpedra_indra'],
		'Credits available current month': [157000],
	}).to_excel(budget_path, index=False)

	result, saved_path = process_licenses_and_credits(
		str(licenses_path), str(credits_path), str(output_path),
		budget_file_path=str(budget_path) if with_budget else None,
	)

	assert result['creditos_base_licencia'].sum() == 58
	assert result['creditos_base'].sum() == (1589 if with_budget else 58)
	assert result['creditos_usados'].sum() == 3
	assert pd.read_excel(saved_path)['creditos_base'].sum() == result['creditos_base'].sum()


def test_apply_budget_increases_rejects_missing_columns(tmp_path):
	budget_path = tmp_path / 'budget.xlsx'
	pd.DataFrame({'User': ['rpedra_indra']}).to_excel(budget_path, index=False)

	with pytest.raises(ValueError, match='credits available current month'):
		apply_budget_increases(pd.DataFrame({'cdalias': ['rpedra'], 'creditos_base': [39]}), str(budget_path))


def test_apply_budget_increases_skips_incomplete_rows(tmp_path):
	budget_path = tmp_path / 'budget.xlsx'
	pd.DataFrame({
		'User': ['rpedra_indra', 'other_indra', None, 'zero_indra'],
		'Credits Available Current Month': [157000, None, 80000, 0],
	}).to_excel(budget_path, index=False)
	users = pd.DataFrame({'cdalias': ['rpedra', 'other', 'zero'], 'creditos_base': [39, 19, 19]})

	result = apply_budget_increases(users, str(budget_path))

	assert result['creditos_base'].tolist() == [1570, 19, 0]


def test_apply_budget_increases_rejects_malformed_matching_amount_with_row(tmp_path):
	budget_path = tmp_path / 'budget.xlsx'
	pd.DataFrame({
		'User': ['rpedra_indra', 'other_indra'],
		'Credits Available Current Month': [157000, 'not a number'],
	}).to_excel(budget_path, index=False)
	users = pd.DataFrame({'cdalias': ['rpedra', 'other'], 'creditos_base': [39, 19]})

	with pytest.raises(ValueError, match='fila\\(s\\): 3'):
		apply_budget_increases(users, str(budget_path))


def test_apply_budget_increases_ignores_malformed_unmatched_amount(tmp_path):
	budget_path = tmp_path / 'budget.xlsx'
	pd.DataFrame({
		'User': ['rpedra_indra', 'other_indra'],
		'Credits Available Current Month': [157000, 'not a number'],
	}).to_excel(budget_path, index=False)
	users = pd.DataFrame({'cdalias': ['rpedra'], 'creditos_base': [39]})

	result = apply_budget_increases(users, str(budget_path))

	assert result['creditos_base'].tolist() == [1570]
