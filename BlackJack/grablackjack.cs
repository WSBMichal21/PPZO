using System;
using System.Collections.Generic;

class Card
{
    public string Suit { get; set; }
    public string Rank { get; set; }

    public Card(string suit, string rank)
    {
        Suit = suit;
        Rank = rank;
    }

    public int Value()
    {
        if (Rank == "J" || Rank == "Q" || Rank == "K")
            return 10;
        if (Rank == "A")
            return 11;

        return int.Parse(Rank);
    }

    public override string ToString()
    {
        return $"{Rank}{Suit}";
    }
}

class Deck
{
    private List<Card> cards = new List<Card>();
    private Random random = new Random();

    public Deck()
    {
        string[] suits = { "♠", "♥", "♦", "♣" };
        string[] ranks = { "2", "3", "4", "5", "6", "7", "8", "9", "10",
                           "J", "Q", "K", "A" };

        foreach (string suit in suits)
        {
            foreach (string rank in ranks)
            {
                cards.Add(new Card(suit, rank));
            }
        }
    }

    public void Shuffle()
    {
        for (int i = cards.Count - 1; i > 0; i--)
        {
            int j = random.Next(i + 1);

            Card temp = cards[i];
            cards[i] = cards[j];
            cards[j] = temp;
        }
    }

    public Card DealCard()
    {
        Card card = cards[cards.Count - 1];
        cards.RemoveAt(cards.Count - 1);
        return card;
    }
}

class Hand
{
    public List<Card> Cards { get; set; }

    public Hand()
    {
        Cards = new List<Card>();
    }

    public void AddCard(Card card)
    {
        Cards.Add(card);
    }

    public int CalculateValue()
    {
        int value = 0;
        int aces = 0;

        foreach (Card card in Cards)
        {
            value += card.Value();

            if (card.Rank == "A")
                aces++;
        }

        while (value > 21 && aces > 0)
        {
            value -= 10;
            aces--;
        }

        return value;
    }

    public override string ToString()
    {
        return string.Join(", ", Cards);
    }
}

class Player
{
    public string Name { get; set; }
    public Hand Hand { get; set; }

    public Player(string name)
    {
        Name = name;
        Hand = new Hand();
    }

    public void Hit(Deck deck)
    {
        Hand.AddCard(deck.DealCard());
    }

    public void Stand()
    {
        Console.WriteLine($"{Name} kończy dobieranie kart.");
    }
}

class Dealer : Player
{
    public Dealer() : base("Dealer")
    {
    }

    public void Play(Deck deck)
    {
        while (Hand.CalculateValue() < 17)
        {
            Hit(deck);
        }
    }
}

class Program
{
    static void Main()
    {
        Deck deck = new Deck();
        deck.Shuffle();

        Player player = new Player("Gracz");
        Dealer dealer = new Dealer();
        
        for (int i = 0; i < 2; i++)
        {
            player.Hit(deck);
            dealer.Hit(deck);
        }

        while (true)
        {
            Console.WriteLine("\nTwoje karty: " + player.Hand);
            Console.WriteLine("Wartość: " + player.Hand.CalculateValue());

            if (player.Hand.CalculateValue() > 21)
            {
                Console.WriteLine("Przegrałeś! Przekroczyłeś 21.");
                return;
            }

            Console.Write("Hit (h) czy Stand (s)? ");
            string choice = Console.ReadLine().ToLower();

            if (choice == "h")
            {
                player.Hit(deck);
            }
            else
            {
                player.Stand();
                break;
            }
        }

        dealer.Play(deck);

        Console.WriteLine("\n=== Wyniki ===");
        Console.WriteLine($"Gracz: {player.Hand} | Wartość: {player.Hand.CalculateValue()}");
        Console.WriteLine($"Dealer: {dealer.Hand} | Wartość: {dealer.Hand.CalculateValue()}");

        int playerValue = player.Hand.CalculateValue();
        int dealerValue = dealer.Hand.CalculateValue();

        if (dealerValue > 21)
            Console.WriteLine("Dealer przekroczył 21. Wygrywasz!");
        else if (playerValue > dealerValue)
            Console.WriteLine("Wygrywasz!");
        else if (playerValue < dealerValue)
            Console.WriteLine("Przegrywasz!");
        else
            Console.WriteLine("Remis!");
    }
}