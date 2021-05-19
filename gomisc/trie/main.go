package main

//https://github.com/dghubble/trie

import "fmt"

type Trie struct {
	value    interface{}
	children map[rune]*Trie
}

func NewTrie() *Trie {
	return new(Trie)
}

func (trie *Trie) Get(key string) interface{} {
	node := trie
	for _, r := range key {
		node = node.children[r]
		if node == nil {
			return nil
		}
	}
	return node.value
}

func (trie *Trie) Put(key string, value interface{}) bool {
	node := trie
	for _, r := range key {
		child, _ := node.children[r]
		if child == nil {
			if node.children == nil {
				node.children = map[rune]*Trie{}
			}
			child = new(Trie)
			node.children[r] = child
		}
		node = child
	}
	isNewVal := node.value == nil
	node.value = value
	return isNewVal
}

func (trie *Trie) Delete(key string) bool {
	path := make([]nodeRune, len(key))
	node := trie
	for i, r := range key {
		path[i] = nodeRune{r: r, node: node}
		node = node.children[r]
		if node == nil {
			return false
		}
	}
	node.value = nil
	if node.isLeaf() {
		for i := len(key) - 1; i >= 0; i-- {
			parent := path[i].node
			r := path[i].r
			delete(parent.children, r)
			if !parent.isLeaf() {
				break
			}
			parent.children = nil
			if parent.value != nil {
				break
			}
		}
	}
	return true
}

type WalkFunc func(key string, value interface{}) error

func (trie *Trie) Walk(walker WalkFunc) error {
	return trie.walk("", walker)
}

func (trie *Trie) WalkPath(key string, walker WalkFunc) error {
	if trie.value != nil {
		if err := walker("", trie.value); err != nil {
			return err
		}
	}

	for i, r := range key {
		if trie = trie.children[r]; trie == nil {
			return nil
		}
		if trie.value != nil {
			if err := walker(string(key[0:i+1]), trie.value); err != nil {
				return err
			}
		}
	}
	return nil
}

type nodeRune struct {
	node *Trie
	r    rune
}

func (trie *Trie) walk(key string, walker WalkFunc) error {
	if trie.value != nil {
		if err := walker(key, trie.value); err != nil {
			return err
		}
	}
	for r, child := range trie.children {
		if err := child.walk(key+string(r), walker); err != nil {
			return err
		}
	}
	return nil
}

func (trie *Trie) isLeaf() bool {
	return len(trie.children) == 0
}

func main() {
	trie := NewTrie()
	const fv = "first"
	cases := []struct {
		key   string
		value interface{}
	}{
		{"dog", 0},
		{"cat", 1},
		{"cats", 2},
		{"dogs", 3},
		{"catdog", 4},
		{"dogcatdog", 5},
		{"/cats", 6},
		{"/cats/garfield", 7},
		{"/dogs/goofy", 8},
	}
	for _, c := range cases {
		if v := trie.Get(c.key); v != nil {
			fmt.Println(c.key, v)
		}
	}

	for _, c := range cases {
		if new := trie.Put(c.key, fv); !new {
			fmt.Println("key exists", c.key)
		}
	}

	for _, c := range cases {
		if new := trie.Put(c.key, c.value); new {
			fmt.Println("key expected", c.key)
		}
	}

	for _, c := range cases {
		if v := trie.Get(c.key); v == c.value {
			fmt.Println(v, c)
		}
	}

	dcases := []struct {
		key   string
		value interface{}
	}{
		{"dog", 0},
		{"dogs", 3},
		{"dogcatdog", 5},
		{"/dogs/goofy", 8},
	}
	for _, d := range dcases {
		if deleted := trie.Delete(d.key); deleted {
			fmt.Println("deleted", d)
		}
	}

	for _, d := range dcases {
		if v := trie.Get(d.key); v == nil {
			fmt.Println("not found", d)
		}
	}

	for _, c := range cases {
		if v := trie.Get(c.key); v == nil {
			fmt.Println("not found", c)
		}
	}

	table := map[string]interface{}{
		"cat":            1,
		"cats":           2,
		"catdog":         4,
		"/cats":          6,
		"/cats/garfield": 7,
	}

	walked := make(map[string]int)
	for k := range table {
		walked[k] = 0
	}
	walker := func(key string, value interface{}) error {
		if value != table[key] {
			fmt.Println("mismatch", value, table[key])
		}
		walked[key]++
		return nil
	}

	if err := trie.Walk(walker); err != nil {
		fmt.Println("walk error", err)
	}

	for k, c := range walked {
		fmt.Println(k,c)
	}
}
