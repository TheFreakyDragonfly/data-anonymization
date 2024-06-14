"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
/* Imports */
const vscode = __importStar(require("vscode"));
const python_shell_1 = require("python-shell");
const path_1 = __importDefault(require("path"));
/* Global Variables */
var used_config;
var used_cs;
var style;
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
/* Action performed when Command is activated */
function activate(context) {
    let disposable = vscode.commands.registerCommand('data-anon-extension.runAnonymisationDialog', () => {
        const panel = vscode.window.createWebviewPanel('anonymisationDialog', 'Data Anonymisation Dialog', vscode.ViewColumn.One, {
            enableScripts: true,
        });
        style = panel.webview.asWebviewUri(vscode.Uri.joinPath(context.extensionUri, 'src', 'css', 'webviews.css'));
        panel.webview.html = getDatabaseSelectionWebviewContent();
        panel.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'open_db_cs':
                    console.log('open db cs:  ' + message.text);
                    used_cs = message.text;
                    connectAndQueryDB_plus_buildSelectionPage(panel);
                    break;
                case 'open_db_config':
                    console.log('open db config:  ' + message.text);
                    used_config = config_string_to_config(message.text);
                    connectAndQueryDB_plus_buildSelectionPage(panel);
                    //write_order("t1");
                    break;
                case 'load_connection_form':
                    panel.webview.html = getDatabaseSelectionWebviewContent();
                    break;
                case 'python':
                    write_order(message.text);
                    panel.webview.html = getDatabaseSelectionWebviewContent();
                    break;
                case 'report':
                    console.log("[Report]: " + message.text);
                    break;
            }
        }, undefined, context.subscriptions);
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
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
						
						vscode.postMessage({
							command: 'open_db_config',
							text: user + ";" + password + ";" + server + ";" + database
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
				</div>
				<button class="open_button" id="config_button" onclick="message_config()">Open</button>
			</body>
		</html>
	`;
}
/* Turns a string into a config */
function config_string_to_config(given_config) {
    let split = given_config.split(";", 4);
    let config = {
        user: split[0],
        password: split[1],
        server: split[2],
        database: split[3],
    };
    return config;
}
/* Builds Table-Selection HTML by connecting to server using global vars */
function connectAndQueryDB_plus_buildSelectionPage(panel) {
    let sql = require("mssql");
    // Establish connection using either config or connectionstring
    let connection_object;
    if (used_cs !== undefined) {
        connection_object = used_cs;
    }
    else if (used_config !== undefined) {
        connection_object = used_config;
    }
    else {
        connection_object = undefined;
    }
    sql.connect(connection_object, function (err) {
        if (err) {
            panel.webview.html += "err: " + err + "<br>";
        }
        let request = new sql.Request();
        request.query('SELECT * FROM INFORMATION_SCHEMA.TABLES', function (err, recordset) {
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
						var active_index = -1;
						var all_tables_status = null;
						var checkbox = null;

						function message_go_back() {
							const vscode = acquireVsCodeApi();

							vscode.postMessage({
								command: 'load_connection_form',
								text: ''
							});
						}

						function hand_over_to_python() {
							const vscode = acquireVsCodeApi();

							let tables = "";
							for(let i = 0; i < all_tables.length; i++) {
								if(all_tables_status[i] == true) {
									tables += all_tables[i].innerHTML + "\\n";
								}
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
							}
						}

						function next_entry() {
							if(active_index !== -1) {
								select(
									all_tables[(active_index + 1) % all_tables.length]
								);
							}
						}

						function checkbox_change() {
							if(checkbox.checked == true) {
								all_tables_status[active_index] = true;
							}
							else {
								all_tables_status[active_index] = false;
							}
						}
					</script>
				</head>
				<body>	
					<div id="list_tables">
			`;
            // ADD Tables to Selection page
            let recordset_by_itself = recordset.recordset;
            let recordset_length = recordset_by_itself.length;
            for (let i = 0; i < recordset_length; i++) {
                constructed_page += '<p class="item_table" onclick="select(this)">';
                constructed_page += recordset_by_itself[i].TABLE_NAME;
                constructed_page += "</p>";
            }
            // SETUP End of Page
            constructed_page += `
					</div>
					<div id="checkbox_and_label">
						<input type="checkbox" id="checkbox_anonymize" onclick="checkbox_change(this)" />
						<label for="checkbox_anonymize">Anonymize</label>
					</div>
					<div id="preview_div"></div>
					<div id="back_button" class="nav_button_round" onclick="message_go_back()">X</div>
					<div id="run_button" class="nav_button_round" onclick="hand_over_to_python()">Run</div>
					<div id="next_button" class="nav_button_round" onclick="next_entry()">></div>
					<script>
						all_tables = document.getElementsByClassName("item_table");
						active_index = 0;
						all_tables[active_index].classList.add("selected_table");
						all_tables_status = Array(all_tables.length).fill(false);
						checkbox = document.getElementById("checkbox_anonymize");
					</script>
				</body>
			</html>
			`;
            panel.webview.html = constructed_page;
        });
    });
}
/* Function calling Python */
function call_python() {
    let options = {
        args: [path_1.default.join(__dirname, 'output')]
    };
    console.log('starting python');
    python_shell_1.PythonShell.run(path_1.default.join(__dirname, '..', '..', 'src', 'order_taker.py'), options).then(messages => {
        console.log('finished python');
    });
}
/* 	Function that writes details for an anonymization order to a file for python.
    Draws Connection details from global vars.
*/
function write_order(tables) {
    const fs = require('fs');
    let path_string = path_1.default.join(__dirname, '..', '..', 'order');
    // Build content of order
    let content = "[Anonymization Order]\n";
    let connection_section;
    if (used_cs !== undefined) {
        connection_section = "[Connection String]\n";
        connection_section += used_cs + "\n";
    }
    else if (used_config !== undefined) {
        connection_section = "[Config]\n";
        connection_section += used_config.user + "\n";
        connection_section += used_config.password + "\n";
        connection_section += used_config.server + "\n";
        connection_section += used_config.database + "\n";
    }
    else {
        connection_section = "erroneus state";
    }
    content += connection_section;
    content += "[TABLES]\n";
    content += tables;
    // Write order to file
    fs.writeFile(path_string, content, function (err) {
        if (err) {
            return console.log(err);
        }
        console.log("The file was saved!");
        call_python();
    });
}
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map