/* Imports */
import * as vscode from 'vscode';
import mssql = require('mssql');
import {PythonShell} from 'python-shell';
import path from 'path';
import { time } from 'console';

/* Global Variables */
var used_config : any | undefined;
var used_cs: string | undefined;
var style : vscode.Uri;
var sql : any;

/* Connection Details for Azure DB; for copy & pasting or testing */
let default_config = {
	user: 'data-anon',
	password: 'Lantanio13891!',
	server: 'sqls-dataanon-dev-001.database.windows.net', 
	database: 'Northwind',
	options: {
		encrypt: true
	}
};
let default_cs = 'Server=tcp:sqls-dataanon-dev-001.database.windows.net,1433;Initial Catalog=Northwind;Persist Security Info=False;User ID=data-anon;Password=Lantanio13891!;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;';

function get_preview(panel : vscode.WebviewPanel, message : any) {
	let request = new sql.Request();

	let headings : string[] = [];
	let contents : string[][] = [];

	request.query(
		"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + message.text + "'",
		(err: Error | AggregateError, recordset: any) => {
	
		if (err) {
			panel.webview.html += "err: " + err + "<br>";
		}

		for(let i = 0; i < recordset.recordset.length; i++) {
			headings.push(recordset.recordset[i].COLUMN_NAME);
		}

		request.query(
			'SELECT TOP 5 * FROM "' + message.text + '"',
			(err: Error | AggregateError, recordset: any) => {
			
			if (err) {
				panel.webview.html += "err: " + err + "<br>";
			}

			for(let i = 0; i < recordset.recordset.length; i++) {
				contents[i] = [];
				
				Object.keys(recordset.recordset[i]).forEach(function(key,index) {
					// key: the name of the object key
					// index: the ordinal position of the key within the object 
					let value = recordset.recordset[i][key];
					if ((value !== null) && (value.length > 50) && !(value instanceof Buffer)) {
						value = value.substring(0, 36);
						value += " ...";
					}
					contents[i].push(value);
				});
			}

			let data = {
				headings: headings,
				contents: contents
			};

			panel.webview.postMessage({ command: 'give_preview', content: data });
		});
	});
}

/* Action performed when Command is activated */
export function activate(context: vscode.ExtensionContext) {
	let disposable = vscode.commands.registerCommand('data-anon-extension.runAnonymisationDialog', () => {
		const panel = vscode.window.createWebviewPanel(
			'anonymisationDialog',
			'Data Anonymisation Dialog',
			vscode.ViewColumn.One,
			{
				enableScripts: true,
			}
		);

		style = panel.webview.asWebviewUri(
			vscode.Uri.joinPath(
				context.extensionUri, 'src', 'css', 'webviews.css'
			)
		);

		panel.webview.html = getDatabaseSelectionWebviewContent();

		panel.webview.onDidReceiveMessage(
			message => {
				switch (message.command) {
					case 'open_db_cs':
						console.log('open db cs:  ' + message.text);

						used_cs = message.text;
						
						connectAndQueryDB_plus_buildSelectionPage(panel);
						break;
					case 'open_db_config':
						console.log('open db config:  ' + message.text);

						used_config = config_string_to_config(message.text);
						console.log(typeof used_config);
						
						connectAndQueryDB_plus_buildSelectionPage(panel);
						break;

					case 'load_connection_form':
						panel.webview.html = getDatabaseSelectionWebviewContent();
						break;

					case 'python':
						write_order(message.text, 0, panel);
						break;

					case 'get_preview':
						get_preview(panel, message);
						
						break;

					case 'report':
						console.log("[Report]: " + message.text);
						break;
				}
			},
			undefined,
        	context.subscriptions
		);
	});

	context.subscriptions.push(disposable);
}

/* Builds HTML for Screen after successful Processing */
function getProcessingFinishedWebviewContent(startingdate: Date, am_tables: number) {
	let time_remaining = (new Date()).getTime() - startingdate.getTime();
	let hours = Math.floor(time_remaining / 3600000); // ms int-div (1000 * 60 * 60)
	time_remaining = time_remaining - hours * 3600000;
	let minutes = Math.floor(time_remaining / 60000);
	time_remaining = time_remaining - minutes * 60000;
	let seconds = Math.floor(time_remaining / 1000);
	time_remaining = time_remaining - seconds * 1000;
	return `
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="UTF-8">
				<title>Test</title>
				<link rel="stylesheet" href="${style}">
				<script>
					const vscode = acquireVsCodeApi();

					function message_continue() {
						vscode.postMessage({
							command: 'load_connection_form',
							text: ''
						});
					}
				</script>
			</head>
			<body>
				<h1 id="page_title">Finished processing!</h1>
				<p id="statistics_heading">Statistics:</p>
				<ul id="statistics_list">
					<li>Anonymized Tables: ${am_tables}</li>
					<li>Used Time: ${hours}h ${minutes}m ${seconds}s</li>
					<li>Amount of LLM Queries: ...</li>
				</ul>
				<button class="open_button" id="continue_button" onclick="message_continue()">Continue</button>
			</body>
		</html>
	`;
}

/* Builds HTML for Database Connecting */
function getDatabaseSelectionWebviewContent() {
	used_cs = undefined;
	used_config = undefined;
	return `
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="UTF-8">
				<title>Test</title>
				<link rel="stylesheet" href="${style}">
				<script>
					const vscode = acquireVsCodeApi();

					function message_default_cs() {
						vscode.postMessage({
							command: 'open_db_cs',
							text: 'Server=tcp:sqls-dataanon-dev-001.database.windows.net,1433;Initial Catalog=Northwind;Persist Security Info=False;User ID=data-anon;Password=Lantanio13891!;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
						});
						show_trying_to_open();
					}

					function message_default_config() {
						vscode.postMessage({
							command: 'open_db_config',
							text: 'data-anon;Lantanio13891!;sqls-dataanon-dev-001.database.windows.net;Northwind'
						});
						show_trying_to_open();
					}

					function message_connectionstring() {
						
						vscode.postMessage({
							command: 'open_db_cs',
							text: document.getElementById("connectionString").value
						});
						show_trying_to_open();
					}
					function message_config() {
						let user = document.getElementById("user").value;
						let password = document.getElementById("password").value;
						let server = document.getElementById("server").value;
						let database = document.getElementById("database").value;
						let trust_server_cert = document.getElementById("checkbox_trust").checked;
						
						vscode.postMessage({
							command: 'open_db_config',
							text: user + ";" + password + ";" + server + ";" + database + ";" + trust_server_cert
						});
						show_trying_to_open();
					}
					function show_trying_to_open() {
						document.body.innerHTML = '<p id="loading">Loading</p>' + '<div id="spinner" class="lds-dual-ring"></div>';
					}
				</script>
			</head>
			<body>
				<h1 id="page_title">Connect to a database</h1>

				<p class="section_title" id="cs_title" onclick="message_default_cs()">Use Connection String</p>
				<div id="cs_and_button">
					<input type="text" class="input_general" id="connectionString" placeholder="Connection String"/>
					<button class="open_button" id="cs_button" onclick="message_connectionstring()">Open</button>
				</div>

				<div id="vertical_line"></div>

				<p id="hint">When connecting you will get a choice on which tables to anonymize.</p>

				<p class="section_title" id="config_title" onclick="message_default_config()">Use SQL-Connection</p>
				<div id="config_inputs_div">
					<input class="input_general" id="user" placeholder="User"/><br>
					<input class="input_general" id="password" placeholder="Password"/><br>
					<input class="input_general" id="server" placeholder="Server"/><br>
					<input class="input_general" id="database" placeholder="Database"/><br>
					<div id="trust_and_label">
						<input type="checkbox" id="checkbox_trust" onclick="" />
						<label for="checkbox_trust">Trust Server Certificate</label>
					</div>
				</div>
				<button class="open_button" id="config_button" onclick="message_config()">Open</button>
			</body>
		</html>
	`;
}

/* Turns a string into a config */
function config_string_to_config(given_config: string) {
	let split = given_config.split(";", 5);
	let config;
	if(split[5] === "false") {
		config = {
			user: split[0],
			password: split[1],
			server: split[2],
			database: split[3],
		};
	}
	else {
		config = {
			user: split[0],
			password: split[1],
			server: split[2],
			database: split[3],
			options: {
				trustServerCertificate: true
			}
		};
	}
	
	return config;
}

/* Builds Table-Selection HTML by connecting to server using global vars */
function connectAndQueryDB_plus_buildSelectionPage(panel: vscode.WebviewPanel) {
	sql = require("mssql");
	console.log(typeof sql);

	// Establish connection using either config or connectionstring
	let connection_object;
	if(used_cs !== undefined) {
		connection_object = used_cs;
	}
	else if(used_config !== undefined) {
		connection_object = used_config;
	}
	else {
		connection_object = undefined;
	}
	sql.connect(connection_object, function (err: Error | AggregateError) {
		if (err) {
			panel.webview.html += "err: " + err + "<br>";
		}
		
		let request = new sql.Request();

		request.query(
			"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA <> 'sys'",
			(err: Error | AggregateError, recordset: any) => {
		
			if (err) {
				panel.webview.html += "err: " + err + "<br>";
			}

			// SETUP Beginning of Page
			let constructed_page = `
			<!DOCTYPE html>
			<html lang="en">
				<head>
					<meta charset="UTF-8">
					<title>Test</title>
					<style>
						ul {
							margin: 0;
							list-style: none;
						}
					</style>
					<link rel="stylesheet" href="${style}">
					<script>
						var all_tables = null;
						var all_markers = null;
						var active_index = -1;
						var all_tables_status = null;
						var checkbox = null;
						var timer = null;
						var preventSimpleClick = null;
						const vscode = acquireVsCodeApi();

						function message_current_preview(tablename) {
							vscode.postMessage({
								command: 'get_preview',
								text: tablename
							});
						}

						function message_go_back() {
							vscode.postMessage({
								command: 'load_connection_form',
								text: ''
							});
						}

						function hand_over_to_python() {
							let tables = "";
							for(let i = 0; i < all_tables.length; i++) {
								if(all_tables_status[i] == true) {
									tables += all_tables[i].innerHTML + "\\n";
								}
							}

							if(tables === "") {
								console.log("first occurance");
								show_warning("No tables selected!");
								return;
							}

							vscode.postMessage({
								command: 'python',
								text: tables
							});
						}

						function select(element) {
							if(element.innerHTML !== all_tables[active_index].innerHTML) {
								for(let i = 0; i < all_tables.length; i++) {
									if(all_tables[i] == element) active_index = i;
									all_tables[i].classList.remove("selected_table");
								}
								element.classList.add("selected_table");

								// Load Content for selection
								checkbox.checked = all_tables_status[active_index];

								// Message  to load preview
								message_current_preview(element.innerHTML)
							}
						}

						function next_entry() {
							if(active_index !== -1) {
								select(
									all_tables[(active_index + 1) % all_tables.length]
								);
							}
						}

						function previous_entry() {
							if(active_index !== -1) {
								let newindex = (active_index - 1);
								if (newindex === -1) {
									newindex = all_tables.length - 1;
								}
								select(all_tables[newindex]);
							}
						}

						function inflict_change(index) {
							if(all_tables_status[index] == false) {
								all_tables_status[index] = true;
								all_markers[index].style.backgroundColor = "green";
								all_markers[index].style.width = "10%";
								all_markers[index].style.left = "45%";
							}
							else {
								all_tables_status[index] = false;
								all_markers[index].style.backgroundColor = "red";
								all_markers[index].style.width = "4%";
								all_markers[index].style.left = "48%";
							}
						}

						function dbl_click_select(element) {
							let found_index = 0;
							for(let i = 0; i < all_tables.length; i++) {
								if(all_tables[i] == element) found_index = i;
							}
							console.log(found_index);
							inflict_change(found_index);
						}

						function checkbox_change() {
							console.log(active_index);
							inflict_change(active_index);
						}

						function single_click(element) {
							select(element);
						}

						function dbl_click(element) {
							dbl_click_select(element);
						}

						window.addEventListener('message', event => {

							const message = event.data; // The JSON data our extension sent

							switch (message.command) {
								case 'give_preview':
									let preview_table = document.getElementById("preview_table");
									preview_table.innerHTML = "";
									let headings = message.content.headings;
									let contents = message.content.contents;
									console.log(headings);

									let header_row = document.createElement("tr");
									for(let i = 0; i < headings.length; i++) {
										let heading = document.createElement("th");
										heading.innerHTML = headings[i];
										header_row.appendChild(heading);
									}
									preview_table.appendChild(header_row);

									for(let i = 0; i < 5 && i < contents.length; i++) {
										let content_row = document.createElement("tr");

										for(let y = 0; y < contents[i].length; y++) {
											let cell = document.createElement("td");
											cell.innerHTML = contents[i][y];
											content_row.appendChild(cell);
										}

										preview_table.appendChild(content_row);
									}

									break;
							}
						});
						async function show_warning(warning) {
							console.log("warning occurance");
							let box = document.getElementById("warning_box");
							box.innerHTML = "Warning! : " + warning;
							box.classList.add("show");
							setTimeout(() => {box.classList.remove("show");}, 4000);
						}
					</script>
				</head>
				<body>	
					<div id="list_tables">
			`;

			// ADD Tables to Selection page
			let recordset_by_itself = recordset.recordset;
			let recordset_length = recordset_by_itself.length;
			for(let i = 0; i < recordset_length; i++) {
				constructed_page += '<div class="div_item_table">';
				constructed_page += '<p class="item_table" onclick="single_click(this)" ondblclick="dbl_click(this)">';
				constructed_page += recordset_by_itself[i].TABLE_NAME;
				constructed_page += "</p>";
				constructed_page += '<div class="item_table_marker"></div>';
				constructed_page += '</div>';
			}

			// SETUP End of Page
			constructed_page += `
					</div>
					<div id="checkbox_and_label">
						<input type="checkbox" id="checkbox_anonymize" onclick="checkbox_change(this)" />
						<label for="checkbox_anonymize">Anonymize</label>
					</div>

					<div id="preview_div">
						<table id="preview_table">
						</table>
					</div>

					<div id="button_container">
						<div id="previous_button" class="nav_button_round" onclick="previous_entry()"><</div>
						<div id="next_button" class="nav_button_round" onclick="next_entry()">></div>

						<!--<div id="run_button" class="nav_button_round" onclick="hand_over_to_python()">Run</div>-->
						<div class="dropdown">
							<button class="dropbtn">Anonymize</button>
							<div class="dropdown-content">
								<a onclick="hand_over_to_python()">Level 1: Pseudonymization</a>
								<a >Level 2: Generalization</a>
							</div>
						</div>

						<div id="back_button" class="nav_button_round" onclick="message_go_back()">X</div>
					</div>
					<script>
						all_tables = document.getElementsByClassName("item_table");
						all_markers = document.getElementsByClassName("item_table_marker");
						active_index = 0;
						all_tables[active_index].classList.add("selected_table");
						all_tables_status = Array(all_tables.length).fill(false);
						checkbox = document.getElementById("checkbox_anonymize");
					</script>

					<div id="warning_box" class="hide">Example text</div>
				</body>
			</html>
			`;

			panel.webview.html = constructed_page;
			get_preview(panel, {
				text: recordset_by_itself[0].TABLE_NAME
			});
		});
	});
}

/* Function calling Python */
function call_python(panel : vscode.WebviewPanel, amount_tables: number) {
	let startingtime = new Date();
	let options = {
		args: [path.join(__dirname, 'output')]
	};
	console.log('starting python');

	let pyshell = new PythonShell(path.join(__dirname, '..', '..', 'data_processing', 'src', 'order_receiver.py'));
	pyshell.on('message', function(message) {
		//always log to console
		console.log(message);

		let parts : String[] = message.split(" ");

		if(parts.length > 2 && parts[0] === "[S]") {
			if(parts[1] === "[CurrentStep]") {
				panel.webview.postMessage({ command: 'current_step', value: message.substring(18) });
			}
			else if(parts[1] === "[CurrentTable]") {
				panel.webview.postMessage({ command: 'current_table', value: message.substring(19) });
			}
			else if(parts[1] === "[OverallProgress]") {
				panel.webview.postMessage({ command: 'overall_progress', value: message.substring(21) });
			}
			else if(parts[1] === "[LLMProgress]") {
				panel.webview.postMessage({ command: 'llm_progress', value: message.substring(17) });
			}
		}
	});

	pyshell.end(function (err, code, signal) {
		if(err) {
			throw err;
		}
		console.log('Exit code: ' + code);
		console.log('Exit signal: ' + signal);
		console.log('finished');
		setTimeout(() => {
			panel.webview.html = getProcessingFinishedWebviewContent(startingtime, amount_tables);
			//panel.webview.html = getDatabaseSelectionWebviewContent();
		}, 1000);
	});
}

/* 	Function that writes details for an anonymization order to a file for python.
	Draws Connection details from global vars.
*/
function write_order(tables: string, limit : number, panel : vscode.WebviewPanel) {
	panel.webview.html = `
	<!DOCTYPE html>
	<html lang="en">
		<head>
			<meta charset="UTF-8">
			<title>Test</title>
			<link rel="stylesheet" href="${style}">
			<script>
				window.addEventListener('message', event => {

					const message = event.data; // The JSON data our extension sent

					switch (message.command) {
						case 'show':
							document.getElementById("currentStep").innerHTML = message.content;
							break;
						case 'tendency':
							let a = (message.value * 100) + '%';
							let b = ((1 - message.value) * 100) + '%';
							let tendency_display = '<span style="color:green;">(' + a + ') Yes</span> ';
							for(let i = 1; i <= 10; i++) {
								if(message.value >= i * 0.1) {
									tendency_display += "+ ";
								}
								else {
									tendency_display += "- ";
								}
							}
							tendency_display += '<span style="color:red;">No (' + b + ')</span>';
							document.getElementById("currentStep").innerHTML =
								"Determining Tendency:<br>" + message.column + "<br>"
								+ tendency_display;
							break;
						case 'current_step':
							document.getElementById("current_step").innerHTML = message.value;
							break;
						case 'current_table':
							document.getElementById("current_table").innerHTML = message.value;
							break;
						case 'overall_progress':
							document.getElementById("overall_progress").innerHTML = message.value;
							break;
						case 'llm_progress':
							document.getElementById("llm_progress").innerHTML = message.value;
							break;
					}
				});
			</script>
		</head>
		<body>
		<p id="loading">Anonymizing</p>
		<div id="spinner" class="lds-dual-ring"></div>
		<p id="current_step" class="info_thingy">...</p>
		<p id="current_table" class="info_thingy">...</p>
		<p id="overall_progress" class="info_thingy">...</p>
		<p id="llm_progress" class="info_thingy">...</p>
		</body>
	</html>
	`;
	const fs = require('fs');

	let path_string = path.join(__dirname, '..', '..', 'order.order');

	// Build content of order
	let content = "[AnonymizationOrder]\n";
	
	let connection_section;
	if(used_cs !== undefined) {
		connection_section = "[Connection CS]\n";
		connection_section += "cs=" + used_cs + "\n";
	}
	else if(used_config !== undefined) {
		connection_section = "[Connection Config]\n";
		connection_section += "server=" + used_config.server + "\n";
		connection_section += "database=" + used_config.database + "\n";
		connection_section += "username=" + used_config.user + "\n";
		connection_section += "password=" + used_config.password + "\n";
		connection_section += "trust=" + used_config.options.trustServerCertificate + "\n";
	}
	else {
		connection_section = "erroneus state";
	}
	content += connection_section;

	content += "[Limit]" + "\n";
	content += "lim=" + limit + "\n";

	content += "[Tables]\n";
	content += tables;

	// Write order to file
	fs.writeFile(path_string, content, (err : Error | AggregateError) => {
		if(err) {
			return console.log(err);
		}
		console.log("The file was saved!");
		let table_amount = tables.split(/\r\n|\r|\n/).length - 1;
		call_python(panel, table_amount);
	}); 
}

export function deactivate() {}
