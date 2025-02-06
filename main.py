import tkinter as tk
from tkinter import messagebox
from bitcoinlib.wallets import Wallet

class UglyWallet:
    def __init__(self, root):
        self.root = root
        self.root.title("Ugly Wallet")
        self.wallets = {}

        self.main_menu()
    
    def main_menu(self):
        self.clear_frame()
        tk.Button(self.root, text="Create Wallet", command=self.creating_wallet).pack(pady=10)
        tk.Button(self.root, text="Browse Wallets", command=self.browse_wallets_page).pack(pady=10)
        tk.Button(self.root, text="Send", command=self.send_page).pack(pady=10)
    
    def creating_wallet(self):
        self.clear_frame()
        tk.Label(self.root, text="Wallet Name").pack()
        wallet_name_entry = tk.Entry(self.root)
        wallet_name_entry.pack()

        def in_fact():
            wallet_name = wallet_name_entry.get().strip()

            if wallet_name:
                try:
                    wallet = Wallet.create(wallet_name, network='testnet')  # Testnet para testes
                    wallet.new_key()
                    wallet.utxos_update()
                    self.wallets[wallet_name] = wallet
                    messagebox.showinfo("Success", f"Wallet '{wallet_name}' created successfully!\nAddress: {wallet.get_key().address}")
                    self.main_menu()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create wallet: {e}")
            else:
                messagebox.showerror("Error", "Wallet name cannot be empty")

        tk.Button(self.root, text="Create", command=in_fact).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    def browse_wallets_page(self):
        self.clear_frame()
        tk.Label(self.root, text="Wallets:").pack()

        if self.wallets:
            for name, wallet in self.wallets.items():
                tk.Label(self.root, text=f"{name}: {wallet.get_key().address}").pack()
        else:
            tk.Label(self.root, text="No wallets created yet.").pack()
        
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)
    
    def send_page(self):
        if not self.wallets:
            messagebox.showerror("Error", "No wallets available. Create one first.")
            return

        self.clear_frame()
        tk.Label(self.root, text="Select Wallet:").pack()

        selected_wallet = tk.StringVar()
        selected_wallet.set("Select a wallet") 

        wallet_options = tk.OptionMenu(self.root, selected_wallet, *self.wallets.keys())
        wallet_options.pack()

        tk.Label(self.root, text="Address:").pack()
        address_entry = tk.Entry(self.root)
        address_entry.pack()

        tk.Label(self.root, text="Amount (BTC):").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        def send_funds():
            wallet_name = selected_wallet.get()
            address = address_entry.get().strip()
            amount = amount_entry.get().strip()

            if wallet_name == "Select a wallet":
                messagebox.showerror("Error", "Please select a valid wallet")
                return
            
            if not address or not amount:
                messagebox.showerror("Error", "Address and Amount cannot be empty")
                return
            
            try:
                amount = float(amount)
                wallet = self.wallets[wallet_name]

                # Checando saldo antes de enviar
                balance = wallet.balance()
                if balance < amount:
                    messagebox.showerror("Error", f"Insufficient balance! Available: {balance} BTC")
                    return
                
                # Realizando transação
                tx = wallet.send_to(address, amount)
                wallet.utxos_update()
                
                messagebox.showinfo("Success", f"Transaction sent!\nTXID: {tx.txid}")
                self.main_menu()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number")
            except Exception as e:
                messagebox.showerror("Error", f"Transaction failed: {e}")

        tk.Button(self.root, text="Send", command=send_funds).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UglyWallet(root)
    root.mainloop()
