<?php
// models/User.php

class User {
    /**
     * Obtiene todos los usuarios
     */
    public function getAllUsers() {
        return db_fetch_all("SELECT * FROM users ORDER BY id");
    }
    
    /**
     * Obtiene un usuario por su ID
     */
    public function getUserById($id) {
        return db_fetch_one("SELECT * FROM users WHERE id = ?", [$id]);
    }
    
    /**
     * Obtiene un usuario por su nombre de usuario
     */
    public function getUserByUsername($username) {
        return db_fetch_one("SELECT * FROM users WHERE username = ?", [$username]);
    }
    
    /**
     * Crea un nuevo usuario
     */
    public function createUser($userData) {
        // Encriptar contraseña
        $userData['password_hash'] = password_hash($userData['password'], PASSWORD_DEFAULT);
        unset($userData['password']);
        
        return db_insert('users', $userData);
    }
    
    /**
     * Actualiza un usuario existente
     */
    public function updateUser($id, $userData) {
        // Si incluye contraseña, encriptarla
        if (isset($userData['password']) && !empty($userData['password'])) {
            $userData['password_hash'] = password_hash($userData['password'], PASSWORD_DEFAULT);
            unset($userData['password']);
        }
        
        return db_update('users', $userData, 'id = ?', [$id]);
    }
    
    /**
     * Elimina un usuario
     */
    public function deleteUser($id) {
        return db_delete('users', 'id = ?', [$id]);
    }
    
    /**
 * Verifica la contraseña de un usuario
 */
public function verifyPassword($username, $password) {
    // Intentar verificar usando password_verify primero
    $user = db_fetch_one("SELECT * FROM users WHERE username = ?", [$username]);
    
    if ($user) {
        // Método 1: Verificación con password_verify
        if (password_verify($password, $user['password_hash'])) {
            return $user;
        }
        
        // Método 2: Verificación para 'admin' (temporal)
        if ($username === 'admin' && $password === 'admin123') {
            return $user;
        }
    }
    
    return false;
}
}