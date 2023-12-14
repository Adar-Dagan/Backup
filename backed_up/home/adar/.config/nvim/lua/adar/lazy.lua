-- Install lazy package manager
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable", -- latest stable release
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    -- Color theme
    { "EdenEast/nightfox.nvim" },

    -- Editor plugins
    { 'nvim-treesitter/nvim-treesitter', build = ':TSUpdate' },
    { 'nvim-telescope/telescope.nvim',   tag = '0.1.3',      dependencies = { 'nvim-lua/plenary.nvim' } },
    { 'nvim-treesitter/playground' },
    { 'theprimeagen/harpoon' },
    { 'mbbill/undotree' },
    { 'tpope/vim-fugitive' },
    { 'github/copilot.vim' },
    { 'tpope/vim-commentary' },
    { 'mfussenegger/nvim-dap' },
    { 'ThePrimeagen/vim-be-good' },
    {
        "j-hui/fidget.nvim",
        opts = {
            -- options
        },
    },

    -- Setup LSP manager
    { 'VonHeikemen/lsp-zero.nvim',        branch = 'v3.x' },

    --- Uncomment these if you want to manage LSP servers from neovim
    { 'williamboman/mason.nvim' },
    { 'williamboman/mason-lspconfig.nvim' },

    -- LSP Support
    {
        'neovim/nvim-lspconfig',
        dependencies = {
            { 'hrsh7th/cmp-nvim-lsp' },
        },
    },

    -- Autocompletion
    {
        'hrsh7th/nvim-cmp',
        dependencies = {
            { 'L3MON4D3/LuaSnip' },
        }
    }
}, {
    git = {
        timeout = 300,
    }
})
